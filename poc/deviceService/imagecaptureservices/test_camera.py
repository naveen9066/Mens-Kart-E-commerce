#!/usr/bin/env python3
"""
Test script for camera connection and image capture
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hikvisionptzcontroller import HikvisionPTZController

def test_camera_connection():
    """Test camera connection and capture"""
    print("Testing Hikvision Camera Connection and Capture")
    print("=" * 50)

    # Camera configuration
    camera_ip = "192.168.1.64"
    username = "admin"
    password = "DWPADMIN123"

    print(f"Connecting to camera: {camera_ip}")
    print(f"Username: {username}")
    print()

    try:
        # Create Hikvision PTZ controller
        print("Creating camera controller...")
        controller = HikvisionPTZController(camera_ip, username, password)
        print("Controller created")
        print()

        # Test connection
        print("Testing connection...")
        if controller.check_health():
            print("Camera connected successfully!")
            print()

            # Test image capture
            print("Testing image capture...")
            save_path = r"C:\Users\Director\Projects\housepulse-main\poc\detectcount\sampleimages"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_capture_{timestamp}.jpg"
            filepath = os.path.join(save_path, filename)

            success = controller.capture_image(filepath)

            if success:
                print("Image captured successfully!")

                # Check if file exists
                if os.path.exists(filepath):
                    file_size = os.path.getsize(filepath)
                    print(f"Image saved: {filename}")
                    print(f"Location: {save_path}")
                    print(f"Size: {file_size} bytes")
                else:
                    print("Warning: Image file not found")

                return True
            else:
                print("Image capture failed")
                return False
        else:
            print("Camera connection failed")
            return False

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    print("Starting Camera Test")
    print()

    success = test_camera_connection()

    print()
    print("=" * 50)
    if success:
        print("Camera test completed successfully!")
        print()
        print("Next steps:")
        print("1. Check the captured image in sampleimages folder")
        print("2. Run detection: cd ../../detectcount && python detectionAnalysisPipelineMain.py")
        print("3. Run full system: cd ../deviceService/imagecaptureservices && python housepulse.py")
    else:
        print("Camera test failed!")
        print()
        print("Troubleshooting:")
        print("1. Check camera IP and credentials")
        print("2. Verify camera is online: ping 192.168.1.64")
        print("3. Check camera web interface: http://192.168.1.64")
        print("4. Ensure hikvisionapi is installed: pip install hikvisionapi")

if __name__ == "__main__":
    main()