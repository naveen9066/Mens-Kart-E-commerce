#!/usr/bin/env python3
"""
Test script for detection pipeline
"""

import os
import sys

def test_detection():
    """Test detection pipeline"""
    print("🔍 Testing Detection Pipeline")
    print("=" * 50)

    # Check if sampleimages folder exists and has images
    sampleimages_path = "sampleimages"
    if not os.path.exists(sampleimages_path):
        print(f"❌ Sample images folder not found: {sampleimages_path}")
        return False

    # List image files
    image_files = [f for f in os.listdir(sampleimages_path)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print("❌ No image files found in sampleimages folder")
        print("💡 Please run camera capture first to generate images")
        return False

    print(f"📁 Found {len(image_files)} image file(s):")
    for img in image_files[:5]:  # Show first 5
        print(f"   - {img}")
    if len(image_files) > 5:
        print(f"   ... and {len(image_files) - 5} more")
    print()

    # Check if detection script exists
    detection_script = "detectionAnalysisPipelineMain.py"
    if not os.path.exists(detection_script):
        print(f"❌ Detection script not found: {detection_script}")
        return False

    print("✅ Detection environment ready!")
    print()
    print("🚀 To run detection:")
    print(f"   python {detection_script}")
    print()
    print("📋 Expected output:")
    print("   - Face detection results")
    print("   - Image quality analysis")
    print("   - PDF report generation")
    print("   - Annotated output images")

    return True

def main():
    """Main test function"""
    print("🏃 Testing Detection Pipeline Setup")
    print()

    success = test_detection()

    print()
    print("=" * 50)
    if success:
        print("🎉 Detection test completed successfully!")
        print()
        print("📋 Next steps:")
        print("1. Run detection: python detectionAnalysisPipelineMain.py")
        print("2. Check output folder for results")
        print("3. Run full system: cd ../deviceService/imagecaptureservices && python housepulse.py")
    else:
        print("💥 Detection test failed!")
        print()
        print("🔧 Troubleshooting:")
        print("1. Ensure images exist in sampleimages folder")
        print("2. Check detection script exists")
        print("3. Verify required packages are installed")

if __name__ == "__main__":
    main()