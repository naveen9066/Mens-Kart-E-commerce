import os
import time
import logging
import schedule
import subprocess
import sys
from datetime import datetime
from configparser import ConfigParser
from hikvisionptzcontroller import HikvisionPTZController

# Fixed save path as per task
SAVE_PATH = r"C:\Users\Director\Projects\housepulse-main\poc\detectcount\sampleimages"
logging.info(f"Image save path: {SAVE_PATH}")

# Test if save path is accessible
try:
    os.makedirs(SAVE_PATH, exist_ok=True)
    test_file = os.path.join(SAVE_PATH, "test_write.tmp")
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    logging.info(f"Save path is writable: {SAVE_PATH}")
except Exception as e:
    logging.error(f"Save path is not accessible: {SAVE_PATH} - {e}")

class HikvisionCameraSDK:
    def __init__(self, ip, username, password, ptz_supported=True):
        self.ip = ip
        self.username = username
        self.password = password
        self.ptz_supported = ptz_supported
        self.controller = None
        self.connect()

    def connect(self):
        """Connect to the Hikvision camera using simple HTTP controller."""
        logging.info(f"[{self.ip}] Attempting to connect to camera...")
        try:
            self.controller = HikvisionPTZController(self.ip, self.username, self.password)
            if self.controller.check_health():
                logging.info(f"[{self.ip}] Successfully connected to Hikvision camera")
                return True
            else:
                logging.error(f"[{self.ip}] Camera connection test failed")
                self.controller = None
                return False
        except Exception as e:
            logging.error(f"[{self.ip}] Failed to connect to camera: {e}")
            import traceback
            logging.error(f"[{self.ip}] Connection traceback: {traceback.format_exc()}")
            self.controller = None
            return False

    def capture_image(self):
        """Capture image and save to fixed path."""
        logging.info(f"[{self.ip}] Attempting to capture image...")
        if not self.controller:
            logging.error(f"[{self.ip}] Camera not connected")
            return False

        try:
            # Use the working controller's capture_image method
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{self.ip.replace('.', '_')}_{timestamp}.jpg"
            filepath = os.path.join(SAVE_PATH, filename)

            # Ensure save directory exists
            os.makedirs(SAVE_PATH, exist_ok=True)

            # Use the controller's capture_image method
            success = self.controller.capture_image(filepath)

            if success:
                logging.info(f"[{self.ip}] Image captured and saved to {filepath}")
                return True
            else:
                logging.error(f"[{self.ip}] Failed to capture image")
                return False
        except Exception as e:
            logging.error(f"[{self.ip}] Exception during image capture: {e}")
            import traceback
            logging.error(f"[{self.ip}] Traceback: {traceback.format_exc()}")
            return False

    def move_ptz(self, pan, tilt, zoom):
        """Move PTZ if supported."""
        if not self.ptz_supported or not self.controller:
            logging.warning("PTZ not supported or camera not connected")
            return False

        try:
            return self.controller.move_ptz(pan, tilt, zoom)
        except Exception as e:
            logging.error(f"Failed to move PTZ: {e}")
            return False

    def get_ptz_status(self):
        """Get current PTZ position."""
        if not self.ptz_supported or not self.controller:
            return None

        try:
            return self.controller.get_ptz_status()
        except Exception as e:
            logging.error(f"Failed to get PTZ status: {e}")
            return None

    def access_web_interface(self):
        """Access web interface."""
        if not self.controller:
            return None

        web_url = f"http://{self.ip}"
        logging.info(f"Web interface URL: {web_url}")
        return web_url

def load_camera_config(config_path):
    """Load camera config from properties file."""
    config = ConfigParser()
    config.optionxform = str
    config.read(config_path)
    cameras = []
    count = int(config.get('Camera', 'camera.count', fallback='0'))
    for i in range(1, count + 1):
        cam = {
            "id": config.get('Camera', f'camera.{i}.id'),
            "ip": config.get('Camera', f'camera.{i}.ip'),
            "username": config.get('Camera', f'camera.{i}.username'),
            "password": config.get('Camera', f'camera.{i}.password'),
            "ptz_supported": config.get('Camera', f'camera.{i}.ptz_supported', fallback='true').lower() == 'true'
        }
        cameras.append(cam)
    return cameras

def capture_all_cameras(cameras):
    """Capture images from all cameras."""
    logging.info(f"Starting capture for {len(cameras)} camera(s)")
    for cam in cameras:
        logging.info(f"Processing camera: {cam['ip']}")
        camera_sdk = HikvisionCameraSDK(cam['ip'], cam['username'], cam['password'], cam['ptz_supported'])
        success = camera_sdk.capture_image()
        if success:
            logging.info(f"Successfully captured image from camera {cam['ip']}")
        else:
            logging.error(f"Failed to capture image from camera {cam['ip']}")

    # Run detection pipeline after capture
    logging.info("Running detection pipeline...")
    run_detection_pipeline()

def run_detection_pipeline():
    """Run the detectcount pipeline."""
    try:
        # Hardcode the correct path for now
        detectcount_dir = r"C:\Users\Director\Projects\housepulse-main\poc\detectcount"

        # Verify the path exists
        if not os.path.exists(detectcount_dir):
            logging.error(f"Detection directory does not exist: {detectcount_dir}")
            return

        pipeline_script = os.path.join(detectcount_dir, "detectionAnalysisPipelineMain.py")

        if not os.path.exists(pipeline_script):
            logging.error(f"Detection script does not exist: {pipeline_script}")
            return

        logging.info(f"Running detection pipeline from {detectcount_dir}...")
        logging.info(f"Script path: {pipeline_script}")

        result = subprocess.run([sys.executable, pipeline_script], cwd=detectcount_dir, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Detection pipeline completed successfully.")
        else:
            logging.error(f"Detection pipeline failed: {result.stderr}")
            logging.error(f"Detection pipeline stdout: {result.stdout}")
    except Exception as e:
        logging.error(f"Error running detection pipeline: {e}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")

def scheduled_capture(cameras):
    """Schedule capture every 10 seconds."""
    schedule.every(10).seconds.do(capture_all_cameras, cameras)

    logging.info("Scheduled capture every 10 seconds. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
    config_path = "camera_config.properties"
    cameras = load_camera_config(config_path)
    if not cameras:
        logging.error("No cameras configured")
        exit(1)

    scheduled_capture(cameras)