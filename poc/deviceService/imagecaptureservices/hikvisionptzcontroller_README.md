# 📹 Hikvision PTZ Controller

## Overview
`hikvisionptzcontroller.py` is the core camera control module for HousePulse, providing comprehensive Hikvision camera integration with PTZ (Pan-Tilt-Zoom) capabilities, image capture, and health monitoring.

## 🎯 **Purpose**
- **Camera Control**: Full PTZ movement and positioning
- **Image Capture**: High-resolution snapshot acquisition
- **Health Monitoring**: Connection status and error recovery
- **Authentication**: Secure Digest authentication support
- **Thread Safety**: Singleton pattern for reliable operation

## 🚀 **Key Features**

### PTZ Control
- ✅ **Absolute Positioning**: Precise pan/tilt/zoom control
- ✅ **Movement Verification**: Confirms position accuracy
- ✅ **Speed Control**: Adjustable movement speeds
- ✅ **Boundary Limits**: Respects camera movement limits

### Image Capture
- ✅ **High Resolution**: Maximum quality snapshots
- ✅ **Stream Support**: Handles large image files
- ✅ **Error Recovery**: Automatic retry on failures
- ✅ **Path Management**: Smart directory handling

### Connection Management
- ✅ **Digest Authentication**: Secure camera access
- ✅ **Health Checks**: Continuous connectivity monitoring
- ✅ **Auto-Reconnection**: Automatic recovery from failures
- ✅ **Thread Safety**: Singleton pattern prevents conflicts

## 🔧 **Technical Implementation**

### Authentication System
```python
# Digest Authentication Setup
from requests.auth import HTTPDigestAuth
self.auth = HTTPDigestAuth(username, password)
```

### Singleton Pattern
```python
# Thread-safe singleton implementation
_instances = {}
_instances_lock = threading.RLock()

@classmethod
def __new__(cls, ip, username, password):
    with cls._instances_lock:
        if ip not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[ip] = instance
        return cls._instances[ip]
```

## 📋 **API Methods**

### PTZ Control
```python
# Move to absolute position
controller.move_ptz(pan=45, tilt=30, zoom=2)

# Move and verify position
success = controller.move_and_verify(45, 30, 2)

# Get current position
position = controller.get_ptz_status()
# Returns: {'pan': 45, 'tilt': 30, 'zoom': 2}
```

### Image Capture
```python
# Capture and save image
success = controller.capture_image("path/to/image.jpg")

# With automatic directory creation
success = controller.capture_image("output/capture.jpg")
```

### Health Monitoring
```python
# Check connection status
is_healthy = controller.check_health()

# Start watchdog monitoring
threading.Thread(target=controller.watchdog, daemon=True).start()
```

## ⚙️ **Configuration**

### Camera Requirements
- **Protocol**: Hikvision ISAPI support
- **Authentication**: Digest authentication enabled
- **Network**: Stable IP connectivity
- **PTZ Support**: Optional (for movement features)

### Connection Parameters
```python
controller = HikvisionPTZController(
    ip="192.168.1.64",
    username="admin",
    password="your_password"
)
```

## 🔄 **Usage Workflow**

### Basic Camera Control
```python
from hikvisionptzcontroller import HikvisionPTZController

# Initialize controller
controller = HikvisionPTZController("192.168.1.64", "admin", "password")

# Check connection
if controller.check_health():
    print("Camera connected successfully")

    # Capture image
    controller.capture_image("capture.jpg")

    # Move PTZ (if supported)
    controller.move_ptz(90, 45, 1)
else:
    print("Camera connection failed")
```

### Advanced PTZ Operations
```python
# Move to specific position with verification
target_pan, target_tilt, target_zoom = 180, 30, 3
if controller.move_and_verify(target_pan, target_tilt, target_zoom):
    print("Position reached successfully")

    # Capture image at new position
    controller.capture_image(f"position_{target_pan}_{target_tilt}.jpg")
```

### Monitoring Setup
```python
# Start health monitoring
import threading
monitor_thread = threading.Thread(
    target=controller.watchdog,
    args=(30,),  # Check every 30 seconds
    daemon=True
)
monitor_thread.start()
```

## 🚨 **Error Handling**

### Connection Issues
```python
try:
    controller = HikvisionPTZController(ip, username, password)
    if not controller.check_health():
        print("Camera not responding")
        # Implement retry logic
except Exception as e:
    print(f"Connection error: {e}")
    # Handle authentication or network errors
```

### PTZ Movement Errors
```python
if not controller.move_and_verify(pan, tilt, zoom):
    print("PTZ movement failed")
    # Check camera PTZ support
    # Verify position limits
    # Implement alternative capture strategy
```

### Image Capture Failures
```python
if not controller.capture_image(filepath):
    print("Image capture failed")
    # Check file permissions
    # Verify disk space
    # Implement retry with different path
```

## 📊 **Performance Characteristics**

### Response Times
- **Health Check**: < 2 seconds
- **Image Capture**: 3-10 seconds (depending on resolution)
- **PTZ Movement**: 5-15 seconds (depending on distance)
- **Position Verification**: < 1 second

### Resource Usage
- **Memory**: ~50MB per controller instance
- **CPU**: Minimal during idle, 10-20% during operations
- **Network**: ~100KB per health check, ~200KB-2MB per image

## 🔧 **Integration Examples**

### With Camera Service
```python
from hikvisionptzcontroller import HikvisionPTZController
from cameracaptureservice import CameraCaptureService

# Initialize camera controller
controller = HikvisionPTZController(ip, username, password)

# Use in capture service
service = CameraCaptureService()
service.capture_with_ptz(controller, ptz_positions)
```

### Batch Processing
```python
# Process multiple positions
positions = [
    (0, 0, 1),    # Home position
    (90, 30, 2),  # Position 1
    (180, 60, 3), # Position 2
]

for pan, tilt, zoom in positions:
    if controller.move_and_verify(pan, tilt, zoom):
        filename = f"capture_{pan}_{tilt}_{zoom}.jpg"
        controller.capture_image(filename)
        print(f"Captured: {filename}")
```

## 🔍 **Troubleshooting**

### Authentication Issues
```bash
# Test with curl
curl -u admin:password http://192.168.1.64/ISAPI/System/status

# Check if Digest auth is required
curl -v http://192.168.1.64/ISAPI/System/status
```

### Network Problems
```bash
# Test connectivity
ping 192.168.1.64

# Check camera web interface
# Open browser: http://192.168.1.64
```

### PTZ Issues
```python
# Check PTZ support
status = controller.get_ptz_status()
if status:
    print(f"PTZ supported, current position: {status}")
else:
    print("PTZ not supported or camera offline")
```

## 📈 **Advanced Features**

### Custom Movement Profiles
```python
def create_ptz_sequence(controller, positions, delays):
    """Execute sequence of PTZ movements with delays"""
    for (pan, tilt, zoom), delay in zip(positions, delays):
        controller.move_and_verify(pan, tilt, zoom)
        time.sleep(delay)
        controller.capture_image(f"sequence_{pan}_{tilt}.jpg")
```

### Monitoring Integration
```python
class CameraMonitor:
    def __init__(self, controller):
        self.controller = controller
        self.status_history = []

    def monitor_health(self, interval=30):
        while True:
            status = self.controller.check_health()
            self.status_history.append({
                'timestamp': datetime.now(),
                'healthy': status
            })
            time.sleep(interval)
```

## 🔄 **Extension Points**

### Custom Authentication
```python
# Override authentication method
class CustomHikvisionController(HikvisionPTZController):
    def __init__(self, ip, username, password, auth_method='digest'):
        super().__init__(ip, username, password)
        if auth_method == 'basic':
            self.auth = (username, password)
        # Add custom auth logic
```

### Enhanced Error Handling
```python
# Add retry mechanism
def capture_with_retry(controller, filepath, max_retries=3):
    for attempt in range(max_retries):
        if controller.capture_image(filepath):
            return True
        print(f"Attempt {attempt + 1} failed, retrying...")
        time.sleep(2)
    return False
```

## 📋 **Best Practices**

### Connection Management
- **Singleton Usage**: Use single controller instance per camera
- **Health Monitoring**: Implement regular health checks
- **Error Recovery**: Handle network interruptions gracefully
- **Resource Cleanup**: Properly close connections when done

### Performance Optimization
- **Batch Operations**: Group multiple operations when possible
- **Async Processing**: Use threading for non-blocking operations
- **Resource Limits**: Monitor memory and network usage
- **Caching**: Cache frequently accessed camera information

### Security Considerations
- **Credential Management**: Store credentials securely
- **Network Security**: Use HTTPS when available
- **Access Logging**: Log all camera access attempts
- **Permission Control**: Limit controller access to authorized users

## 🎯 **API Reference**

### Constructor
```python
HikvisionPTZController(ip, username, password)
# ip: Camera IP address
# username: Camera username
# password: Camera password
```

### Core Methods
- `check_health()` → bool: Check camera connectivity
- `capture_image(filepath)` → bool: Capture and save image
- `move_ptz(pan, tilt, zoom)` → bool: Move to absolute position
- `move_and_verify(pan, tilt, zoom)` → bool: Move and verify position
- `get_ptz_status()` → dict: Get current PTZ position
- `watchdog(interval)`: Start health monitoring thread

### Utility Methods
- `ensure_connection()`: Reconnect if connection lost
- `reboot_camera()`: Reboot camera remotely
- `wait_until_online(timeout)`: Wait for camera to come online

---

**Hikvision PTZ Controller** - Your gateway to professional camera control! 📹🎛️