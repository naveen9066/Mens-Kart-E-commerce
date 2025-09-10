import os
import time
import threading
import logging
from hikvision_camera_sdk import load_camera_config, scheduled_capture
from logsetup import setup_logging

setup_logging()  # This will create /log and set up logging
logging.getLogger().setLevel(logging.DEBUG)  # Enable debug logging

def health_beat():
    while True:
        logging.info("[HEALTH BEAT] Camera capture service is running.")
        time.sleep(300)  # 5 minutes

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    camera_config_path = os.path.join(root_dir, "camera_config.properties")

    threading.Thread(target=health_beat, daemon=True, name="HealthBeatThread").start()

    cameras = load_camera_config(camera_config_path)
    if not cameras:
        logging.error("No cameras configured")
        return

    scheduled_capture(cameras)

if __name__ == "__main__":
    main()