# 🏠 HousePulse - Automated Camera Surveillance & Face Detection System

HousePulse is an intelligent surveillance system that integrates Hikvision cameras with advanced face detection and analytics capabilities. The system automatically captures images, detects faces, analyzes image quality, and generates comprehensive reports for deployment monitoring.

## 🎯 **System Overview**

HousePulse combines:
- **Automated Camera Capture**: Hikvision camera integration with 10-second intervals
- **Face Detection**: Advanced RetinaFace-based face detection and counting
- **Quality Analysis**: Image quality metrics and focus analysis
- **Report Generation**: PDF reports with analytics and visualizations
- **Real-time Monitoring**: Health checks and automated processing

## 🚀 **Quick Start**

### Prerequisites
```bash
pip install -r requirement.txt
```

### Basic Usage
```bash
# Test camera connection
cd poc/deviceService/imagecaptureservices
python test_camera.py

# Run detection pipeline
cd ../../poc/detectcount
python detectionAnalysisPipelineMain.py

# Start full automated system
cd ../deviceService/imagecaptureservices
python housepulse.py
```

## 📁 **Project Structure**

```
housepulse-main/
├── poc/
│   ├── deviceService/
│   │   └── imagecaptureservices/     # Camera capture services
│   │       ├── hikvisionptzcontroller.py    # Hikvision SDK controller
│   │       ├── cameracaptureservice.py      # Main camera service
│   │       ├── test_camera.py              # Camera testing script
│   │       ├── housepulse.py               # Main orchestrator
│   │       ├── camera_config.properties    # Camera configuration
│   │       └── jobschedule.properties      # Schedule configuration
│   └── detectcount/                        # Face detection & analysis
│       ├── detectionAnalysisPipelineMain.py # Main detection pipeline
│       ├── ImageQualityAnalysis.py         # Quality analysis module
│       ├── generatePdfReport.py            # PDF report generation
│       └── sampleimages/                   # Image storage & output
│           ├── output/                     # Processed results
│           └── *.jpg                       # Captured images
├── requirement.txt                         # Python dependencies
└── README.md                              # This file
```

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

## 🎥 **Camera Integration**

### Features
- ✅ **Hikvision SDK Integration**: Official Python SDK support
- ✅ **Digest Authentication**: Secure camera authentication
- ✅ **PTZ Control**: Pan-Tilt-Zoom camera movement
- ✅ **Health Monitoring**: Automatic connection monitoring
- ✅ **Scheduled Capture**: Configurable capture intervals
- ✅ **Fixed Path Storage**: No automatic subfolder creation

### Testing Camera
```bash
cd poc/deviceService/imagecaptureservices
python test_camera.py
```

## 🔍 **Face Detection & Analysis**

### Features
- ✅ **RetinaFace Integration**: High-accuracy face detection
- ✅ **Batch Processing**: Process multiple images automatically
- ✅ **Quality Metrics**: Sharpness, contrast, noise analysis
- ✅ **PDF Reports**: Comprehensive analytics reports
- ✅ **Annotated Output**: Images with face bounding boxes

### Running Detection
```bash
cd poc/detectcount
python detectionAnalysisPipelineMain.py
```

## 📊 **System Output**

### Generated Files
- **Annotated Images**: `sampleimages/output/*_counted.jpg`
- **PDF Report**: `sampleimages/output/report.pdf`
- **Quality Metrics**: Integrated in PDF report

### Sample Results
```
Processing: test_capture_20250909_210025.jpg
✅ Faces detected: 2
📊 Quality Score: 85.4%
📄 PDF report saved: ./sampleimages/output/report.pdf
🚀 Pipeline completed successfully!
```

## 🔧 **Technical Details**

### Dependencies
```txt
hikvisionapi==0.3.2
opencv-python==4.8.1.78
retinaface==0.0.13
deepface==0.0.79
reportlab==4.0.7
schedule==1.2.0
tensorflow==2.15.0
matplotlib==3.8.2
```

### Authentication
- **Digest Authentication**: Required for Hikvision cameras
- **Fallback Support**: Direct HTTP requests when SDK fails
- **Thread Safety**: Singleton pattern for camera connections

### Performance
- **Capture Interval**: 10 seconds (configurable)
- **Processing Time**: ~30-60 seconds per image batch
- **Memory Usage**: Optimized for continuous operation
- **Error Recovery**: Automatic reconnection on failures

## 🚨 **Troubleshooting**

### Camera Issues
```bash
# Test network connectivity
ping 192.168.1.64

# Check camera web interface
# Open browser: http://192.168.1.64
```

### Common Problems
- **Connection Failed**: Verify IP, username, password in config
- **Authentication Error**: Ensure Digest auth is supported
- **Path Issues**: Check write permissions for save directory
- **SDK Errors**: Update hikvisionapi if compatibility issues

### Logs
- Check console output for detailed error messages
- Enable debug logging in configuration files
- Monitor `sampleimages/output/` for processing results

## 📈 **Analytics & Reporting**

### PDF Report Contents
- Face detection results with counts
- Image quality metrics and charts
- Processing timestamps and performance data
- Annotated image thumbnails
- Summary statistics and trends

### Integration Points
- Camera service saves images every 10 seconds
- Detection pipeline processes new images automatically
- PDF reports generated with each batch
- Real-time monitoring through health checks

## 🔄 **Deployment Node Payload Schema**

*Previous documentation for cloud integration schema follows...*

## 🧩 Root-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `deploymentNodeId` | string | Unique identifier for the edge device deployment node. |
| `deploymentNodeName` | string | Human-readable name for the deployment site. |
| `type` | string | Type of deployment (e.g., multiplex, school, factory). |
| `deploymentRegion` | string | Region or zone where the node is installed. |
| `firmwareVersion` | string | Current firmware version running on the edge device. |
| `dataTimestamp` | string (ISO 8601) | Timestamp when the data was captured. |
| `requestId` | string | Unique ID for this data transmission session. |
| `eventType` | string | Indicates reason for the capture (routine, anomaly, manual). |
| `subUnits` | array | List of subunits monitored by this node (e.g., screens, classrooms). |

## 🧱 SubUnit Object

| Field | Type | Description |
|-------|------|-------------|
| `subUnitId` | string | Unique identifier for this subunit (zone/screen/classroom). |
| `subUnitName` | string | Descriptive name for this specific subunit. |
| `type` | string | Type/category of the subunit (e.g., screen, classroom). |
| `expectedCameras` | integer | Total cameras expected to respond in this subunit. |
| `responseSummary` | object | Summary of response from cameras in the subunit. |
| `environmental` | object | Captures ambient conditions like light and temperature. |
| `cameras` | array | List of camera devices monitoring this subunit. |

### 📊 `responseSummary` Object

| Field | Type | Description |
|-------|------|-------------|
| `total` | integer | Total number of cameras assigned to this subunit. |
| `responded` | integer | Number of cameras that responded with valid data. |
| `responsePercentage` | float | % of cameras that responded (for analytics/alerts). |

### 🌡️ `environmental` Object

| Field | Type | Description |
|-------|------|-------------|
| `ambientLight` | string | Detected ambient light condition (e.g., "low", "normal"). |
| `temperatureC` | float | Ambient temperature in Celsius. |

## 🎥 Camera Object

| Field | Type | Description |
|-------|------|-------------|
| `cameraId` | string | Unique identifier for the camera. |
| `status` | string | Response status of the camera ("responded", "no response"). |
| `latencyMs` | integer | Response latency of the camera in milliseconds. |
| `powerStatus` | string | Power source or state (e.g., wired, battery, unknown). |
| `anomalyFlagged` | boolean | Whether an anomaly was detected for this camera. |
| `data` | object | Captured data (if response is successful). |

### 🖼️ `data` Object

| Field | Type | Description |
|-------|------|-------------|
| `imageUrl` | string | URL to the captured image or frame. |
| `occupancy` | integer | Number of occupants detected in the frame. |
| `frameHash` | string | SHA or MD5 hash of the image frame for integrity. |
| `anomalies` | array (optional) | List of anomalies detected (e.g., "low light"). |

---

This schema is versionable, auditable, and extensible across domains such as smart classrooms, multiplexes, or factory floors.



```json
{
  "deploymentNodeId": "node-001",
  "deploymentNodeName": "Deployment Site Alpha",
  "type": "multiplex",
  "deploymentRegion": "IN-TN-SHL", 
  "firmwareVersion": "v2.3.1",
  "dataTimestamp": "2025-07-01T16:41:00Z",
  "requestId": "req-8723a98c6d",
  "eventType": "routineCapture",
  "subUnits": [
    {
      "subUnitId": "su-01",
      "subUnitName": "Screen 1",
      "type": "screen",
      "expectedCameras": 3,
      "responseSummary": {
        "total": 3,
        "responded": 2,
        "responsePercentage": 66.7
      },
      "environmental": {
        "ambientLight": "low",
        "temperatureC": 24.5
      },
      "cameras": [
        {
          "cameraId": "Cam001",
          "status": "responded",
          "latencyMs": 152,
          "powerStatus": "wired",
          "anomalyFlagged": false,
          "data": {
            "imageUrl": "http://example.com/image1.jpg",
            "occupancy": 50,
            "frameHash": "9f8ab3ee719cbd8d554fa7"
          }
        },
        {
          "cameraId": "Cam002",
          "status": "responded",
          "latencyMs": 189,
          "powerStatus": "battery",
          "anomalyFlagged": true,
          "data": {
            "imageUrl": "http://example.com/image2.jpg",
            "occupancy": 45,
            "frameHash": "8a9d6a1e328fdea07b392c",
            "anomalies": ["low light"]
          }
        },
        {
          "cameraId": "Cam003",
          "status": "no response",
          "powerStatus": "unknown",
          "anomalyFlagged": true
        }
      ]
    }
  ]
}
```

# 🧾 Naming Conventions for Deployment Node Payload Variables

This guide defines consistent naming rules for variables used in the deployment payload schema. Following these conventions ensures readability, maintainability, and interoperability across systems.

---

## 🧱 General Naming Guidelines

| Rule | Description |
|------|-------------|
| **Camel Case** | Use camelCase for all variable names (e.g., `cameraId`, `dataTimestamp`). |
| **Descriptive & Concise** | Variable names should be short yet clearly convey their purpose. |
| **No Abbreviations** | Avoid ambiguous abbreviations unless well-established (e.g., `latencyMs` is acceptable, but avoid `tSp` for timestamp). |
| **Singular Form** | Use singular nouns for objects (`cameraId`), plural for arrays (`subUnits`). |
| **Consistent Prefixes** | Use clear prefixes to convey the context (e.g., `deploymentNodeId`, `subUnitId`, `cameraId`). |
| **No Special Characters** | Stick to letters, numbers, and capitalization—no spaces, hyphens, or underscores. |

---

## 🧩 Variable Naming Rules

| Variable Name | Type | Naming Rule |
|---------------|------|-------------|
| `deploymentNodeId` | string | Starts with `deploymentNode`, ends with `Id` to denote unique identifier |
| `deploymentNodeName` | string | Describes the site name in a readable format |
| `type` | string | Generic field to describe classification (e.g., "school", "factory") |
| `deploymentRegion` | string | ISO or human-readable regional code (e.g., `IN-TN-SHL`) |
| `firmwareVersion` | string | Alphanumeric with version prefixes (e.g., `v1.0.3`) |
| `dataTimestamp` | string | Must follow ISO 8601 format; variable starts with `data` for clarity |
| `requestId` | string | Use a UUID or hash; prefix with `request` |
| `eventType` | string | Indicates action origin using camelCase (e.g., `routineCapture`) |
| `subUnits` | array | Plural, indicates a collection of sub-units or zones |

---

## 🧱 Sub-Unit Fields

| Variable Name | Type | Naming Rule |
|---------------|------|-------------|
| `subUnitId` | string | Unique, prefixed with `subUnit` |
| `subUnitName` | string | Human-readable label for easy identification |
| `expectedCameras` | integer | Prefix describes intent (expected vs actual count) |
| `responseSummary` | object | Summarizes response health; uses camelCase for nested fields |
| `environmental` | object | Groups ambient data like temperature and lighting |
| `type` | string | Mirrors root-level `type` to classify subunit |

---

## 🎥 Camera Fields

| Variable Name | Type | Naming Rule |
|---------------|------|-------------|
| `cameraId` | string | Unique identifier for the camera, prefixed with `camera` |
| `status` | string | Lowercase keywords only (`responded`, `no response`) |
| `latencyMs` | integer | Suffix `Ms` denotes time in milliseconds |
| `powerStatus` | string | Values: `wired`, `battery`, `unknown`; describes power source |
| `anomalyFlagged` | boolean | Prefix with `anomaly`, verb-style naming for flagging |
| `data` | object | Nested object for media capture metadata |

---

## 🖼️ Captured Data Fields

| Variable Name | Type | Naming Rule |
|---------------|------|-------------|
| `imageUrl` | string | Use `Url` suffix for clarity; valid URL string |
| `occupancy` | integer | Count of people or objects detected |
| `frameHash` | string | Cryptographic hash string for verifying frame integrity |
| `anomalies` | array | Describes all issues identified in frame (optional) |

---

By adhering to these naming conventions, you'll ensure that your data pipelines, edge-device firmware, and cloud services remain clean, consistent, and future-ready.


