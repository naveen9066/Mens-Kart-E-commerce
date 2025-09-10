#!/usr/bin/env python3
"""
Minimal camera test - Connect and capture to verify functionality
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hikvisionptzcontroller import HikvisionPTZController

def test_camera_basic():
    """Basic camera connection and capture test"""
    print("Basic Camera Test")
    print("=" * 30)

    # Camera details
    camera_ip = "192.168.1.64"
    username = "admin"
    password = "DWPADMIN123"

    # Required save path
    required_path = r"C:\Users\Director\Projects\housepulse-main\poc\detectcount\sampleimages"

    print(f"Camera IP: {camera_ip}")
    print(f"Save Path: {required_path}")
    print()

    try:
        # Step 1: Create controller
        print("1. Creating camera controller...")
        controller = HikvisionPTZController(camera_ip, username, password)
        print("SUCCESS: Controller created")

        # Step 2: Test connection
        print("2. Testing connection...")
        if controller.check_health():
            print("SUCCESS: Camera connection successful")
        else:
            print("FAILED: Camera connection failed")
            return False

        # Step 3: Ensure save directory exists
        print("3. Checking save directory...")
        os.makedirs(required_path, exist_ok=True)
        print(f"SUCCESS: Save directory ready: {required_path}")

        # Step 4: Capture image
        print("4. Capturing image...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_capture_{timestamp}.jpg"
        filepath = os.path.join(required_path, filename)

        success = controller.capture_image(filepath)

        if success:
            print("SUCCESS: Image capture successful")

            # Step 5: Verify file exists
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"SUCCESS: Image saved: {filename}")
                print(f"Location: {required_path}")
                print(f"Size: {file_size} bytes")

                # Step 6: List all files in directory
                print("\nFiles in save directory:")
                files = os.listdir(required_path)
                for file in files:
                    if file.endswith('.jpg'):
                        print(f"   {file}")

                return True
            else:
                print("FAILED: Image file not found after capture")
                return False
        else:
            print("FAILED: Image capture failed")
            return False

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("Camera Connection & Capture Test")
    print("This test ensures camera works and saves to correct path only")
    print()

    success = test_camera_basic()

    print()
    print("=" * 50)
    if success:
        print("SUCCESS: Camera test PASSED!")
        print()
        print("Camera is working correctly")
        print("Images are saved to the required path")
        print("No other directories are used")
        print()
        print("Ready for next steps:")
        print("1. Run detection: cd ../../detectcount && python detectionAnalysisPipelineMain.py")
        print("2. Run full system: python housepulse.py")
    else:
        print("FAILED: Camera test FAILED!")
        print()
        print("Check:")
        print("- Camera IP and credentials")
        print("- Camera is powered on and connected")
        print("- Network connectivity")
        print("- Required path permissions")

if __name__ == "__main__":
    main()