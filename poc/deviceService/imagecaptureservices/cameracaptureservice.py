import os
import time
import json
import logging
from datetime import datetime
from configparser import ConfigParser
import threading

CAMERA_SECTION = 'Camera'

def load_camera_config(config_path):
    """
    Loads camera configuration from a .properties file.
    Returns a list of camera dicts.
    """
    config = ConfigParser()
    config.optionxform = str
    config.read(config_path)
    cameras = []
    count = int(config.get(CAMERA_SECTION, 'camera.count', fallback='0'))
    for i in range(1, count + 1):
        cam = {
            "id": config.get(CAMERA_SECTION, f'camera.{i}.id'),
            "ip": config.get(CAMERA_SECTION, f'camera.{i}.ip'),
            "username": config.get(CAMERA_SECTION, f'camera.{i}.username'),
            "password": config.get(CAMERA_SECTION, f'camera.{i}.password'),
            "image_store_path": config.get(CAMERA_SECTION, f'camera.{i}.image_store_path', fallback='./captures'),
            "interval": int(config.get(CAMERA_SECTION, f'camera.{i}.interval', fallback='60')),
            "certificate": config.get(CAMERA_SECTION, f'camera.{i}.certificate', fallback=None),
            "auth_type": config.get(CAMERA_SECTION, f'camera.{i}.auth_type', fallback="basic"),
            "ptz_supported": config.get(CAMERA_SECTION, f'camera.{i}.ptz_supported', fallback="true")
        }
        cameras.append(cam)
    return cameras

def load_ptz_positions(camera_id, blobstore_dir):
    """
    Loads PTZ positions from the camera's JSON file.
    """
    json_path = os.path.join(blobstore_dir, f"{camera_id}.json")
    with open(json_path, "r") as f:
        data = json.load(f)
    # Support both single and multiple camera blobs
    if isinstance(data, list):
        for cam in data:
            if str(cam.get("camera_id")) == str(camera_id):
                return [(p["pan"], p["tilt"], p["zoom"]) for p in cam["ptz_positions"]]
    elif isinstance(data, dict):
        return [(p["pan"], p["tilt"], p["zoom"]) for p in data.get("ptz_positions", [])]
    return []

def load_job_schedule(schedule_path, camera_id):
    """
    Loads interval value for a camera from jobschedule.prop file.
    """
    config = ConfigParser()
    config.optionxform = str
    config.read(schedule_path)
    interval = config.get('DEFAULT', f'camera.{camera_id}.interval', fallback=None)
    return int(interval) if interval else None

def batch_ptz_capture(controller, ptz_list, save_dir=".", max_retries=2, delay=2):
    """
    Move PTZ to each (pan, tilt, zoom), capture image, and return list of image paths.
    Retries failed moves/captures at the end up to max_retries times.

    Args:
        controller (HikvisionPTZController): Initialized PTZ controller object.
        ptz_list (list): List of (pan, tilt, zoom) tuples.
        save_dir (str): Directory to save images.
        max_retries (int): Number of retries for failed positions.
        delay (int): Seconds to wait after move before capture.

    Returns:
        List[str]: List of image file paths (in order of ptz_list).
    """
    logging.debug(f"[batch_ptz_capture] Starting batch capture. PTZ list: {ptz_list}, save_dir: {save_dir}, max_retries: {max_retries}, delay: {delay}")

    # Use HikvisionPTZController for PTZ operations
    results = [None] * len(ptz_list)
    failures = []

    for idx, (pan, tilt, zoom) in enumerate(ptz_list):
        img_path = f"{save_dir}/ptz_{pan}_{tilt}_{zoom}.jpg"
        logging.debug(f"[batch_ptz_capture] Attempting move to pan={pan}, tilt={tilt}, zoom={zoom} (index {idx})")
        if controller.move_and_verify(pan, tilt, zoom):
            logging.debug(f"[batch_ptz_capture] Move successful for pan={pan}, tilt={tilt}, zoom={zoom}")
            time.sleep(delay)
            if controller.capture_image(img_path):
                results[idx] = img_path
                logging.info(f"[batch_ptz_capture] Captured image: {img_path}")
            else:
                logging.warning(f"[batch_ptz_capture] Image capture failed at {pan},{tilt},{zoom}")
                failures.append((idx, pan, tilt, zoom))
        else:
            logging.warning(f"[batch_ptz_capture] PTZ move failed at {pan},{tilt},{zoom}")
            failures.append((idx, pan, tilt, zoom))

    # Retry failures
    for attempt in range(max_retries):
        if not failures:
            logging.debug(f"[batch_ptz_capture] No failures to retry after attempt {attempt}.")
            break
        logging.info(f"[batch_ptz_capture] Retrying {len(failures)} failed positions (attempt {attempt+1})")
        new_failures = []
        for idx, pan, tilt, zoom in failures:
            img_path = f"{save_dir}/ptz_{pan}_{tilt}_{zoom}_retry{attempt+1}.jpg"
            logging.debug(f"[batch_ptz_capture] Retry attempt {attempt+1} for pan={pan}, tilt={tilt}, zoom={zoom} (index {idx})")
            if controller.move_and_verify(pan, tilt, zoom):
                logging.debug(f"[batch_ptz_capture] Retry move successful for pan={pan}, tilt={tilt}, zoom={zoom}")
                time.sleep(delay)
                if controller.capture_image(img_path):
                    results[idx] = img_path
                    logging.info(f"[batch_ptz_capture] Captured image (retry): {img_path}")
                else:
                    logging.warning(f"[batch_ptz_capture] Image capture failed at {pan},{tilt},{zoom} (retry)")
                    new_failures.append((idx, pan, tilt, zoom))
            else:
                logging.warning(f"[batch_ptz_capture] PTZ move failed at {pan},{tilt},{zoom} (retry)")
                new_failures.append((idx, pan, tilt, zoom))
        failures = new_failures
        logging.debug(f"[batch_ptz_capture] Failures remaining after attempt {attempt+1}: {failures}")

    logging.debug(f"[batch_ptz_capture] Batch capture complete. Results: {results}")
    return results

class CameraCaptureService:
    @staticmethod
    def camera_capture_worker_with_stats(cam, blobstore_dir, jobschedule_path, stats_dict):
        camera_id = cam["id"]
        thread_name = threading.current_thread().name
        logging.debug(f"[{thread_name}] Starting worker for Camera {camera_id}")
        stats_dict[camera_id] = {
            "images": [],
            "start_time": datetime.now(),
            "end_time": None,
            "total_captures": 0,
            "failures": 0
        }
        ip = cam["ip"]
        username = cam["username"]
        password = cam["password"]
        certificate = cam.get("certificate")
        auth_type = cam.get("auth_type", "basic")
        ptz_supported = cam.get("ptz_supported", "true").lower() == "true"
        store_path = cam["image_store_path"]

        interval = load_job_schedule(jobschedule_path, camera_id) or cam["interval"]
        logging.info(f"[{thread_name}] Camera {camera_id}: ip={ip}, cert={certificate}, auth={auth_type}, ptz_supported={ptz_supported}, store={store_path}, interval={interval}")

        controller = HikvisionPTZController(ip, username, password)
        logging.debug(f"[{thread_name}] HikvisionPTZController initialized for Camera {camera_id}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use fixed store_path, no subfolder creation
        save_dir = store_path
        os.makedirs(save_dir, exist_ok=True)  # Ensure directory exists
        logging.debug(f"[{thread_name}] Using save directory: {save_dir}")

        if ptz_supported:
            ptz_list = load_ptz_positions(camera_id, blobstore_dir)
            logging.debug(f"[{thread_name}] Loaded PTZ positions: {ptz_list}")
            if not ptz_list:
                logging.warning(f"[{thread_name}] No PTZ positions found for camera {camera_id}")
            else:
                logging.info(f"[{thread_name}] Capturing PTZ images for camera {camera_id} at {save_dir}")
                images = batch_ptz_capture(controller, ptz_list, save_dir=save_dir)
                logging.debug(f"[{thread_name}] batch_ptz_capture returned: {images}")
                stats_dict[camera_id]["images"].extend([img for img in images if img])
                stats_dict[camera_id]["total_captures"] += len([img for img in images if img])
                stats_dict[camera_id]["failures"] += len([img for img in images if not img])
                logging.info(f"[{thread_name}] Completed PTZ capture for camera {camera_id}")
        else:
            img_path = os.path.join(save_dir, f"{camera_id}_simple_{timestamp}.jpg")
            logging.info(f"[{thread_name}] Capturing simple image for camera {camera_id} at {img_path}")
            success = controller.capture_image(img_path)
            logging.debug(f"[{thread_name}] capture_image returned: {success}")
            if success:
                stats_dict[camera_id]["images"].append(img_path)
                stats_dict[camera_id]["total_captures"] += 1
                logging.info(f"[{thread_name}] Simple image captured for camera {camera_id}")
            else:
                stats_dict[camera_id]["failures"] += 1
                logging.error(f"[{thread_name}] Simple image capture failed for camera {camera_id}")

        stats_dict[camera_id]["end_time"] = datetime.now()
        elapsed = stats_dict[camera_id]["end_time"] - stats_dict[camera_id]["start_time"]
        logging.info(f"[{thread_name}] Finished. Time taken: {elapsed}")
        logging.debug(f"[{thread_name}] Stats for Camera {camera_id}: {stats_dict[camera_id]}")

def scheduled_camera_capture(camera_config_path, blobstore_dir, jobschedule_path):
    """
    Starts one thread per camera for scheduled capture.
    Each thread is named and logs its name.
    At the end, logs a summary of images captured and time taken for each camera.
    Adds debug logs for cameras found and more detailed progress.
    If no cameras found, logs and exits without starting threads.
    """
    cameras = load_camera_config(camera_config_path)
    logging.info(f"CAMERAS FOUND: {len(cameras)}")
    if not cameras:
        logging.error("No cameras found in configuration. Exiting scheduled_camera_capture.")
        return

    for idx, cam in enumerate(cameras, 1):
        logging.debug(f"Camera {idx}: ID={cam['id']}, IP={cam['ip']}, PTZ Supported={cam.get('ptz_supported', 'true')}, Store Path={cam['image_store_path']}")

    threads = []
    capture_stats = {}

    for cam in cameras:
        logging.info(f"Spawning thread for Camera ID={cam['id']} (IP={cam['ip']})")
        thread = threading.Thread(
            target=CameraCaptureService.camera_capture_worker_with_stats,
            args=(cam, blobstore_dir, jobschedule_path, capture_stats),
            name=f"CameraThread-{cam['id']}"
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)

    logging.info("All camera threads started. Waiting for completion...")

    for thread in threads:
        logging.debug(f"Waiting for thread {thread.name} to finish.")
        thread.join()
        logging.debug(f"Thread {thread.name} finished.")

    # Log summary
    logging.info("=== Capture Summary ===")
    for cam_id, stats in capture_stats.items():
        elapsed = stats["end_time"] - stats["start_time"] if stats["end_time"] and stats["start_time"] else "N/A"
        logging.info(
            "Camera %s: Images captured: %d, Failures: %d, Time taken: %s, Files: %s",
            cam_id,
            stats['total_captures'],
            stats['failures'],
            elapsed,
            ', '.join(stats['images'])
        )
# Example usage:
scheduled_camera_capture(
     camera_config_path="/path/to/camera_config.properties",
     blobstore_dir="/path/to/cameraptzblobstore",
     jobschedule_path="/path/to/jobschedule.prop"
 )