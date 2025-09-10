# 🎥 Hikvision Camera Setup and Integration

## Overview
This module handles Hikvision camera integration using the official Python SDK for automated image capture in the HousePulse surveillance system. The system captures images every 10 seconds and saves them to a fixed path for processing by the detection pipeline.

## ✅ **Latest Changes**
- **Digest Authentication**: Fixed authentication to use Digest auth instead of Basic auth
- **SDK Optimization**: Updated `hikvisionptzcontroller.py` with direct HTTP fallbacks
- **10-Second Intervals**: Configured for frequent capture intervals
- **Fixed Path Storage**: All images saved to `C:\Users\Director\Projects\housepulse-main\poc\detectcount\sampleimages`
- **No Subfolders**: Eliminated automatic folder creation for clean storage
- **Thread Safety**: Singleton pattern for reliable camera connections

## 📋 **Prerequisites**
1. **Install Dependencies**:
   ```bash
   pip install hikvisionapi schedule requests
   ```

2. **Camera Requirements**:
   - Hikvision IP camera with ISAPI support
   - Network connectivity to camera
   - Valid camera credentials (Digest authentication)

3. **System Requirements**:
   - Python 3.8+
   - Write permissions to save directory
   - Network access to camera IP

## ⚙️ **Configuration**

### Camera Configuration (`camera_config.properties`)
```properties
[Camera]
camera.count=1
camera.1.id=1
camera.1.ip=192.168.1.64
camera.1.username=admin
camera.1.password=DWPADMIN123
camera.1.ptz_supported=true
camera.1.image_store_path=C:\Users\Director\Projects\housepulse-main\poc\detectcount\sampleimages
```

### Schedule Configuration (`jobschedule.properties`)
```properties
[DEFAULT]
camera.1.interval=10
```

## 🎯 **Features**

- ✅ **Digest Authentication**: Secure authentication for Hikvision cameras
- ✅ **PTZ Control**: Full pan-tilt-zoom capabilities (if supported)
- ✅ **Health Monitoring**: Automatic connection status checks
- ✅ **Scheduled Capture**: Configurable capture intervals (currently 10 seconds)
- ✅ **Thread Safety**: Singleton pattern prevents connection conflicts
- ✅ **Error Recovery**: Automatic reconnection on failures
- ✅ **Fixed Path Storage**: No automatic subfolder creation

## 🧪 **Testing Camera Connection**

### Quick Test
```bash
cd poc/deviceService/imagecaptureservices
python test_camera.py
```

**Expected Output:**
```
Testing Hikvision Camera Connection and Capture
==================================================
Connecting to camera: 192.168.1.64
Username: admin

Creating camera controller...
Controller created

Testing connection...
Camera connected successfully!

Testing image capture...
Image captured successfully!
Image saved: test_capture_20250909_210025.jpg
Location: C:\Users\Director\Projects\housepulse-main\poc\detectcount\sampleimages
Size: 225205 bytes

Camera test completed successfully!
```

## 🚀 **Running the Camera Service**

### Start Full System
```bash
cd poc/deviceService/imagecaptureservices
python housepulse.py
```

### Manual Capture Test
```bash
cd poc/deviceService/imagecaptureservices
python camera_test_only.py
```

### What Happens
1. **Connection**: Establishes secure connection to Hikvision camera
2. **Health Check**: Monitors camera connectivity every 30 seconds
3. **Capture**: Takes images every 10 seconds automatically
4. **Storage**: Saves all images to fixed path without subfolders
5. **Integration**: Images ready for detection pipeline processing

## 🔧 **Troubleshooting**

### Connection Issues
```bash
# Test network connectivity
ping 192.168.1.64

# Check camera web interface
# Open browser: http://192.168.1.64
```

### Common Problems
- **❌ Connection Failed**: Verify IP, username, password in `camera_config.properties`
- **❌ Authentication Error**: Ensure camera supports Digest authentication
- **❌ Path Permission Error**: Check write permissions for save directory
- **❌ SDK Compatibility**: Update hikvisionapi if version conflicts occur
- **❌ PTZ Not Working**: Verify PTZ support on your camera model

### Debug Steps
1. **Check Camera Access**:
   ```bash
   curl -u admin:DWPADMIN123 http://192.168.1.64/ISAPI/System/status
   ```

2. **Verify Configuration**:
   - Ensure IP address is correct
   - Confirm username/password are valid
   - Check save path exists and is writable

3. **Test Individual Components**:
   ```bash
   python test_camera.py          # Test basic connection
   python camera_test_only.py     # Test capture functionality
   ```

## 🔗 **Integration with Detection Pipeline**

### Automatic Workflow
1. **Camera Service** captures images every 10 seconds
2. **Images saved** to `poc/detectcount/sampleimages/`
3. **Detection Pipeline** processes new images automatically
4. **PDF Reports** generated with analytics
5. **Annotated images** saved to `output/` folder

### Manual Processing
```bash
# Process captured images
cd ../../poc/detectcount
python detectionAnalysisPipelineMain.py
```

### Output Files
- **Annotated Images**: `sampleimages/output/*_counted.jpg`
- **PDF Report**: `sampleimages/output/report.pdf`
- **Quality Metrics**: Integrated in PDF with charts

## 📊 **Performance & Monitoring**

### System Metrics
- **Capture Interval**: 10 seconds (configurable)
- **Image Size**: ~200-300KB per image
- **Processing Time**: 30-60 seconds per batch
- **Memory Usage**: Optimized for continuous operation

### Health Monitoring
- **Connection Status**: Checked every 30 seconds
- **Automatic Recovery**: Reconnects on failures
- **Error Logging**: Detailed logs for troubleshooting
- **Thread Safety**: Singleton pattern prevents conflicts

## 🔄 **Configuration Updates**

### Changing Capture Interval
Edit `jobschedule.properties`:
```properties
[DEFAULT]
camera.1.interval=30  # Change to 30 seconds
```

### Adding Multiple Cameras
Update `camera_config.properties`:
```properties
[Camera]
camera.count=2
camera.1.id=1
camera.1.ip=192.168.1.64
# ... camera 1 config ...

camera.2.id=2
camera.2.ip=192.168.1.65
# ... camera 2 config ...
```