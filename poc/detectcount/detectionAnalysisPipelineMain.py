import cv2
import os
import numpy as np
import logging
from PIL import Image
from tqdm import tqdm
from retinaface import RetinaFace
from deepface import DeepFace
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table
from reportlab.lib import colors
from ImageQualityAnalysis import analyze_quality, get_metrics_chart, get_focus_heatmap, get_intensity_histogram
from generatePdfReport import generate_pdf, add_metrics_explanation_page

# ================================
# ⚙️ Configuration Flags
# ================================
CONFIG = {
    "input_folder": "./sampleimages",
    "threshold": 0.1,
    "show_box": True,
    "show_gender": False,
    "enable_face_detection": True,
    "enable_gender": False,
    "enable_human_detection": True,
    "enable_quality": True,
    "enable_pdf": True,
    "human_threshold": 0.1
}

# ================================
# 🔧 Setup Logger
# ================================
def setup_logger(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=level
    )

# ================================
# 📁 File Handling
# ================================
def get_image_files(folder):
    return [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

def prepare_directories(input_path):
    output_path = os.path.join(input_path, "output")
    os.makedirs(output_path, exist_ok=True)
    return output_path


# ================================
# 🖍️ Drawing Boxes
# ================================
def draw_boxes(image, faces=None, human_boxes=None, gender_results=None,
               show_box=True, show_gender=False, enable_gender=False):
    if human_boxes:
        for person in human_boxes:
            x1, y1, x2, y2 = person["bbox"]
            conf = person["confidence"]
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, f"Human ({conf:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    if faces:
        for key in faces:
            x1, y1, x2, y2 = faces[key]["facial_area"]
            if show_box:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if show_gender and enable_gender:
                gender, confidence = gender_results.get(key, ("Unknown", 0))
                label = f"{gender} ({confidence:.1f}%)"
                cv2.putText(image, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    label_text = f"Faces: {len(faces) if faces else 0} | Humans: {len(human_boxes) if human_boxes else 0}"
    cv2.putText(image, label_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

    return image

# ================================
# 🧍‍♂️ Human Detection via YOLOv8
# ================================
def detect_humans(image, model, threshold=0.3):
    results = model(image)
    boxes = []
    for det in results[0].boxes.data.cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if int(cls) == 0 and conf >= threshold:
            boxes.append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "confidence": float(conf)
            })
    return boxes

def detect_objects(image, model, threshold=0.3):
    results = model(image)
    boxes = {"person": [], "chair": []}
    for det in results[0].boxes.data.cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        label = int(cls)
        if conf < threshold:
            continue
        if label == 0:  # 'person' class
            boxes["person"].append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "confidence": float(conf)
            })
        elif label == 57:  # COCO 'chair' class
            boxes["chair"].append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "confidence": float(conf)
            })
    return boxes

def calculate_iou(boxA, boxB):
    xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
    xB, yB = min(boxA[2], boxB[2]), min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return interArea / (boxAArea + boxBArea - interArea + 1e-5)

def infer_occupancy(person_boxes, chair_boxes, threshold=0.3):
    count = 0
    occupied_chairs = []
    for chair in chair_boxes:
        for person in person_boxes:
            iou = calculate_iou(person["bbox"], chair["bbox"])
            if iou >= threshold:
                count += 1
                occupied_chairs.append(chair)
                break
    return count, occupied_chairs


# ================================
# 🚀 Main Pipeline
# ================================
def run_pipeline(config):
    setup_logger(logging.DEBUG)
    input_folder = config["input_folder"]
    output_folder = prepare_directories(input_folder)
    image_files = get_image_files(input_folder)
    pdf_path = os.path.join(output_folder, "report.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4) if config["enable_pdf"] else None

    quality_stats = {}  # Initialize to avoid UnboundLocalError
    for file_name in image_files:
        image_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_counted.jpg")
        logging.info(f"📁 Processing: {file_name}")
        image = cv2.imread(image_path)
        if image is None:
            logging.error("❌ Image failed to load")
            continue

        faces = {}
        if config["enable_face_detection"]:
            faces = RetinaFace.detect_faces(image_path, threshold=config["threshold"])
            logging.debug(f"🟩 Faces detected: {len(faces)}")

        gender_results = {}
        if config["enable_gender"]:
            for key in faces:
                x1, y1, x2, y2 = faces[key]["facial_area"]
                try:
                    crop = image[y1:y2, x1:x2]
                    result = DeepFace.analyze(crop, actions=["gender"], enforce_detection=False)
                    gender = result[0]["gender"]
                    confidence = result[0]["gender_confidence"]
                    gender_results[key] = (gender, confidence)
                except:
                    gender_results[key] = ("Unknown", 0)


        quality_stats, heatmap, gray = analyze_quality(image, file_name) if config["enable_quality"] else ({}, None, None)

        # 🖼️ Overlay annotations
        image = draw_boxes(
            image=image,
            faces=faces,
            gender_results=gender_results,
            show_box=config["show_box"],
            show_gender=config["show_gender"],
            enable_gender=config["enable_gender"]
        )

        # 💾 Save output image
        cv2.imwrite(output_path, image)
        logging.info(f"✅ Output saved: {output_path}")

        # 📄 Generate PDF report page
        if config["enable_pdf"] and c and quality_stats:
            generate_pdf(
                c,
                image_path,
                output_path,
                quality_stats,
                face_count=len(faces),
                heatmap=heatmap,
                gray=gray
            )

    # 🧷 Finalize PDF
    if config["enable_pdf"] and c:
        # Add the explanation page ONCE after all images/pages are done
        add_metrics_explanation_page(c, quality_stats, A4[0], A4[1])
        c.save()
        logging.info(f"\n📄 PDF report saved: {pdf_path}")
    logging.info("🚀 Pipeline completed successfully!")
    
# ================================
# 🚦 Run Script
# ================================
if __name__ == "__main__":
    run_pipeline(CONFIG)
