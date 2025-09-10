"""
Hikvision PTZ Controller Service

Provides PTZ movement, status, health checks, image capture, and reboot for Hikvision cameras via ISAPI.
"""

import threading
import logging
from hikvisionapi import Client
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPDigestAuth
import time

logging.basicConfig(level=logging.INFO)

class HikvisionPTZController:
    """
    Thread-safe Hikvision PTZ camera controller.
    Singleton per IP: one instance per camera IP.
    """
    _instances = {}
    _instances_lock = threading.Lock()

    def __new__(cls, ip, username, password):
        with cls._instances_lock:
            if ip not in cls._instances:
                logging.debug(f"[HikvisionPTZController] Creating new instance for IP: {ip}")
                instance = super(HikvisionPTZController, cls).__new__(cls)
                instance._initialized = False
                cls._instances[ip] = instance
            else:
                logging.debug(f"[HikvisionPTZController] Returning existing instance for IP: {ip}")
        return cls._instances[ip]

    def __init__(self, ip, username, password):
        if getattr(self, "_initialized", False):
            logging.debug(f"[HikvisionPTZController] Instance for {ip} already initialized.")
            return
        logging.debug(f"[HikvisionPTZController] Initializing instance for {ip}")
        self.ip = ip
        self.client = Client(f"http://{ip}", username, password)
        self.auth = HTTPDigestAuth(username, password)
        self._lock = threading.RLock()
        self._initialized = True
        logging.info(f"Initialized HikvisionPTZController for {ip}")

    def move_ptz(self, pan, tilt, zoom):
        """
        Send absolute PTZ move command.
        Args:
            pan (int): Azimuth (horizontal angle)
            tilt (int): Elevation (vertical angle)
            zoom (int): Absolute zoom value
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            logging.debug(f"[{self.ip}] move_ptz called with pan={pan}, tilt={tilt}, zoom={zoom}")
            payload = f"""
            <PTZData>
                <AbsoluteHigh>
                    <azimuth>{pan}</azimuth>
                    <elevation>{tilt}</elevation>
                    <absoluteZoom>{zoom}</absoluteZoom>
                </AbsoluteHigh>
            </PTZData>
            """
            try:
                response = self.client.put('/ISAPI/PTZCtrl/channels/1/absolute', data=payload.encode('utf-8'))
                success = response.status_code == 200
                logging.info(f"[{self.ip}] PTZ move command sent: pan={pan}, tilt={tilt}, zoom={zoom}, success={success}")
                logging.debug(f"[{self.ip}] PTZ move response: {response.status_code}, {response.content}")
                return success
            except Exception as e:
                logging.error(f"[{self.ip}] Exception during PTZ move: {e}")
                return False

    def get_ptz_status(self):
        """
        Fetch current PTZ position.
        Returns:
            dict: {'pan': int, 'tilt': int, 'zoom': int} or None if failed
        """
        with self._lock:
            logging.debug(f"[{self.ip}] get_ptz_status called")
            try:
                response = self.client.get('/ISAPI/PTZCtrl/channels/1/status')
                logging.debug(f"[{self.ip}] PTZ status response: {response.status_code}, {response.content}")
                if response.status_code != 200:
                    logging.error(f"[{self.ip}] Failed to retrieve PTZ status.")
                    return None
                root = ET.fromstring(response.content)
                azimuth = root.find('.//azimuth').text
                elevation = root.find('.//elevation').text
                zoom = root.find('.//absoluteZoom').text
                status = {
                    'pan': int(azimuth),
                    'tilt': int(elevation),
                    'zoom': int(zoom)
                }
                logging.info(f"[{self.ip}] PTZ status: {status}")
                return status
            except Exception as e:
                logging.error(f"[{self.ip}] Exception during get_ptz_status: {e}")
                return None

    def move_and_verify(self, target_pan, target_tilt, target_zoom, tolerance=2):
        """
        Move PTZ and verify position within tolerance.
        Args:
            target_pan (int), target_tilt (int), target_zoom (int), tolerance (int)
        Returns:
            bool: True if position matches within tolerance, False otherwise
        """
        with self._lock:
            logging.debug(f"[{self.ip}] move_and_verify called with target_pan={target_pan}, target_tilt={target_tilt}, target_zoom={target_zoom}, tolerance={tolerance}")
            if not self.move_ptz(target_pan, target_tilt, target_zoom):
                logging.error(f"[{self.ip}] PTZ movement failed.")
                return False
            status = self.get_ptz_status()
            if not status:
                logging.error(f"[{self.ip}] Could not verify PTZ position.")
                return False
            match = (
                abs(status['pan'] - target_pan) <= tolerance and
                abs(status['tilt'] - target_tilt) <= tolerance and
                abs(status['zoom'] - target_zoom) <= tolerance
            )
            logging.info(f"[{self.ip}] Moved to: {status}, Match: {match}")
            logging.debug(f"[{self.ip}] move_and_verify result: {match} (expected: pan={target_pan}, tilt={target_tilt}, zoom={target_zoom}, got: {status})")
            return match

    def check_health(self):
        """
        Check if camera is healthy (online).
        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            logging.debug(f"[{self.ip}] check_health called")
            # Try using direct HTTP request as fallback
            import requests
            url = f"http://{self.ip}/ISAPI/System/status"
            response = requests.get(url, auth=self.auth, timeout=10)
            healthy = response.status_code == 200
            logging.info(f"[{self.ip}] Health check: {'OK' if healthy else 'FAILED'}")
            logging.debug(f"[{self.ip}] Health check response: {response.status_code}")
            return healthy
        except Exception as e:
            logging.error(f"[{self.ip}] Health check failed: {e}")
            return False

    def ensure_connection(self):
        """
        Ensure connection to camera, reinitialize if needed.
        """
        try:
            logging.debug(f"[{self.ip}] ensure_connection called")
            _ = self.client.get('/ISAPI/System/status')
        except Exception:
            logging.warning(f"[{self.ip}] Reinitializing connection to camera...")
            self.client = Client(self.client.host, self.client.user, self.client.pwd)

    def watchdog(self, interval=30):
        """
        Watchdog thread to monitor camera health and reconnect if needed.
        Args:
            interval (int): Time in seconds between checks
        """
        logging.info(f"[{self.ip}] Starting watchdog thread with interval {interval}s...")
        while True:
            if not self.check_health():
                self.ensure_connection()
            time.sleep(interval)

    def capture_image(self, save_path="snapshot.jpg"):
        """
        Capture highest resolution snapshot from channel 1 using direct HTTP request.
        Args:
            save_path (str): Path to save the image
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            logging.debug(f"[{self.ip}] capture_image called, saving to {save_path}")
            try:
                # Use direct HTTP request instead of hikvisionapi
                import requests
                import os

                url = f"http://{self.ip}/ISAPI/Streaming/channels/1/picture"

                # Ensure directory exists
                dir_path = os.path.dirname(save_path)
                if dir_path:  # Only create directory if path is not empty
                    os.makedirs(dir_path, exist_ok=True)

                response = requests.get(url, auth=self.auth, stream=True, timeout=30)
                logging.debug(f"[{self.ip}] Image capture response: {response.status_code}")

                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                    # Verify file was saved
                    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                        logging.info(f"[{self.ip}] Image saved to {save_path}")
                        return True
                    else:
                        logging.error(f"[{self.ip}] Image file not saved properly")
                        return False
                else:
                    logging.error(f"[{self.ip}] Failed to capture image, HTTP {response.status_code}")
                    return False
            except Exception as e:
                logging.error(f"[{self.ip}] Exception during image capture: {e}")
                return False

    def reboot_camera(self):
        """
        Reboot camera via ISAPI.
        Returns:
            bool: True if successful, False otherwise
        """
        with self._lock:
            logging.debug(f"[{self.ip}] reboot_camera called")
            url = f"http://{self.ip}/ISAPI/System/reboot"
            xml_data = '<reboot><delayTime>1</delayTime></reboot>'
            try:
                response = requests.put(url, data=xml_data, auth=self.auth, headers={'Content-Type': 'application/xml'})
                success = response.status_code == 200
                logging.info(f"[{self.ip}] Reboot command sent, success={success}")
                logging.debug(f"[{self.ip}] Reboot response: {response.status_code}, {response.content}")
                return success
            except Exception as e:
                logging.error(f"[{self.ip}] Exception during reboot: {e}")
                return False

    def wait_until_online(self, timeout=60):
        """
        Poll for camera availability after reboot.
        Args:
            timeout (int): Seconds to wait before giving up
        Returns:
            bool: True if camera is online, False otherwise
        """
        url = f"http://{self.ip}/ISAPI/System/status"
        start = time.time()
        logging.debug(f"[{self.ip}] wait_until_online called, timeout={timeout}s")
        while time.time() - start < timeout:
            try:
                response = requests.get(url, auth=self.auth)
                if response.status_code == 200:
                    logging.info(f"[{self.ip}] Camera is back online.")
                    return True
            except Exception as e:
                logging.debug(f"[{self.ip}] Polling camera status: {e}")
            logging.info(f"[{self.ip}] Waiting for camera...")
            time.sleep(2)
        logging.error(f"[{self.ip}] Camera did not come back online in time.")
        return False

# Example usage:
controller = HikvisionPTZController("192.168.1.64", "admin", "DWPADMIN123")
controller.move_ptz(10, 20, 5)
controller.capture_image("snapshot.jpg")
threading.Thread(target=controller.watchdog, daemon=True).start()




