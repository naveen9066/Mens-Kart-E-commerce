# 🔍 DetectCount - Face Detection & Image Analysis Module

## Overview
DetectCount is the intelligent image processing module of HousePulse that analyzes captured surveillance images to detect faces, assess image quality, and generate comprehensive analytics reports. It seamlessly integrates with the camera capture service for automated processing.

## ✅ **Latest Updates**
- **Path Fix**: Corrected input folder path for proper image discovery
- **Batch Processing**: Processes all JPG images in the sampleimages folder
- **Quality Metrics**: Enhanced image quality analysis with focus and sharpness detection
- **PDF Generation**: Comprehensive reports with charts and annotations
- **Integration**: Automatic processing of camera-captured images

## 📋 **Prerequisites**

### Dependencies Installation
```bash
pip install retinaface deepface opencv-python pillow tqdm reportlab scikit-image matplotlib tensorflow
```

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 4GB+ RAM recommended for batch processing
- **Storage**: Sufficient space for processed images and PDF reports
- **GPU**: Optional but recommended for faster processing

### Input Requirements
- **Image Format**: JPG/JPEG files only
- **Location**: `sampleimages/` folder (relative to detectcount directory)
- **Naming**: Any valid filename (timestamps recommended)

## ⚙️ **Configuration**

### Main Configuration (`detectionAnalysisPipelineMain.py`)
```python
CONFIG = {
    "input_folder": "./sampleimages",     # Input directory
    "threshold": 0.1,                    # Face detection confidence
    "show_box": True,                    # Draw bounding boxes
    "show_gender": False,                # Show gender detection
    "enable_face_detection": True,       # Enable face detection
    "enable_gender": False,              # Enable gender analysis
    "enable_human_detection": True,      # Enable human detection
    "enable_quality": True,              # Enable quality analysis
    "enable_pdf": True,                  # Generate PDF reports
    "human_threshold": 0.1               # Human detection threshold
}
```

### Quality Analysis Parameters
- **Sharpness**: Focus and blur detection
- **Contrast**: Image contrast measurement
- **Noise**: Image noise level assessment
- **Brightness**: Overall brightness analysis

## 🎯 **Features**

### Core Capabilities
- ✅ **Advanced Face Detection**: RetinaFace with high accuracy and speed
- ✅ **Batch Processing**: Process multiple images automatically
- ✅ **Quality Analysis**: Comprehensive image quality metrics
- ✅ **PDF Report Generation**: Professional reports with charts and analytics
- ✅ **Annotation Output**: Images with face bounding boxes and labels
- ✅ **Real-time Integration**: Automatic processing of camera captures

### Detection Technologies
- **RetinaFace**: State-of-the-art face detection algorithm
- **DeepFace**: Gender and emotion analysis (optional)
- **OpenCV**: Image processing and annotation
- **TensorFlow**: Neural network processing backend

## 🧪 **Testing Detection Setup**

### Environment Check
```bash
cd poc/detectcount
python test_detection.py
```

### Manual Test Run
```bash
cd poc/detectcount
python detectionAnalysisPipelineMain.py
```

**Expected Output:**
```
📁 Processing: test_capture_20250909_210025.jpg
🟩 Faces detected: 2
📊 Quality Score: 85.4%
📄 PDF report saved: ./sampleimages/output/report.pdf
🚀 Pipeline completed successfully!
```

## 🚀 **Running Detection Pipeline**

### Automated Processing
```bash
cd poc/detectcount
python detectionAnalysisPipelineMain.py
```

### Processing Workflow
1. **Discovery**: Scans `sampleimages/` for JPG files
2. **Face Detection**: RetinaFace analyzes each image
3. **Quality Analysis**: Computes sharpness, contrast, noise metrics
4. **Annotation**: Draws bounding boxes on detected faces
5. **Report Generation**: Creates PDF with analytics and charts
6. **Output**: Saves annotated images and PDF to `output/` folder

### Processing Results
```
📁 Processing: 4.jpeg
🟩 Faces detected: 9
📊 Quality Score: 87.2%

📁 Processing: 5.jpeg
🟩 Faces detected: 212
📊 Quality Score: 82.1%

📁 Processing: test_capture_20250909_210025.jpg
🟩 Faces detected: 2
📊 Quality Score: 85.4%

📄 PDF report saved: ./sampleimages/output/report.pdf
🚀 Pipeline completed successfully!
```

## Output Structure
- **Input Images**: Original captured images in `sampleimages/`
- **Output Images**: Annotated images with face boxes in `sampleimages/output/`
- **PDF Report**: Comprehensive report with metrics and visualizations in `sampleimages/output/report.pdf`

## Integration with Camera Service
- Camera service saves images to `sampleimages/` every 10 seconds
- DetectCount automatically processes new images when run
- No manual intervention required for batch processing

## Troubleshooting
- **No Images Found**: Ensure images are in JPG format and located in `sampleimages/`
- **Face Detection Issues**: Adjust threshold in CONFIG if needed
- **PDF Generation Errors**: Check write permissions for output directory
- **Memory Issues**: For large batches, process in smaller chunks

## Customization
- Modify `CONFIG` in `detectionAnalysisPipelineMain.py` to enable/disable features
- Adjust quality analysis parameters in `ImageQualityAnalysis.py`
- Customize PDF layout in `generatePdfReport.py`

## Performance Tips
- Process images in batches to manage memory usage
- Use GPU acceleration for faster face detection (if available)
- Monitor disk space for output files