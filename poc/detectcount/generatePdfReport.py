from PIL import Image
from reportlab.lib.pagesizes import A2
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table
from reportlab.lib import colors
from ImageQualityAnalysis import get_focus_heatmap, get_intensity_histogram

METRIC_EXPLANATIONS = {
    "File Name": "The name of the image file.",
    "Resolution": "Width × height of the image in pixels.",
    "Aspect Ratio": "Ratio of width to height.",
    "Total Pixels": "Total number of pixels in the image.",
    "Megapixels": "Image size in millions of pixels.",
    "Sharpness": "How clear or crisp the image is.",
    "Noise Level": "Amount of random variation in brightness or color.",
    "Contrast": "Difference between the darkest and brightest parts.",
    "Dynamic Range": "Range of brightness levels captured.",
    "Entropy": "Amount of information or detail in the image.",
    "Mean Brightness": "Average brightness of all pixels.",
    "Edge Density": "How many edges (details) are present.",
    "Fully In Focus": "Whether the whole image is sharp.",
    "Focus Coverage": "Percentage of the image that is in focus.",
    "Colorfulness": "How vivid or intense the colors are.",
    "Saturation": "Intensity of colors.",
    "White Balance Deviation": "How much the color balance differs from neutral.",
    "Overall Quality": "Summary of image quality based on all metrics."
}

def generate_pdf(
    c, image_path, output_path, stats,
    face_count,
    heatmap=None, gray=None
):
    # Use A2 size for more space
    page_width, page_height = A2
    c.setPageSize((page_width, page_height))

    margin = 50
    section_gap = 40

    # Title and Info
    y = page_height - margin
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, f"Report: {stats.get('File Name', 'N/A')}")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Input: {image_path}")
    c.drawString(page_width - margin - 300, y, f"Output: {output_path}")
    y -= section_gap

    # Images side by side, dynamically sized
    img = Image.open(image_path)
    out_img = Image.open(output_path)
    img_area_width = (page_width - 3 * margin) // 2
    img_area_height = min(300, page_height // 4)
    img.thumbnail((img_area_width, img_area_height))
    out_img.thumbnail((img_area_width, img_area_height))
    img_y = y - img.height
    c.drawImage(ImageReader(img), margin, img_y, width=img.width, height=img.height)
    c.drawImage(ImageReader(out_img), margin * 2 + img_area_width, img_y, width=out_img.width, height=out_img.height)
    y = img_y - section_gap

    # Metrics Table (horizontal, dynamic col width)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Metrics")
    y -= 30
    c.setFont("Helvetica", 10)
    keys = list(stats.keys())
    values = [str(stats[k]) for k in keys]
    table_data = [keys, values]
    col_width = max(80, (page_width - 2 * margin) // len(keys))
    table = Table(table_data, colWidths=[col_width] * len(keys))
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    table_height = 40  # Approximate, adjust if needed
    table.wrapOn(c, page_width, page_height)
    table.drawOn(c, margin, y - table_height)
    y = y - table_height - section_gap

    # Detection counts
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, f"Detected Faces: {face_count}")
    y -= 20
    # Removed humans count
    # if chair_count is not None:
    #     y -= 20
    #     c.drawString(margin, y, f"Detected Chairs: {chair_count}")
    # if occupancy_count is not None:
    #     y -= 20
    #     c.drawString(margin, y, f"Occupied Chairs: {occupancy_count}")
    y -= section_gap

    # Charts in one row, dynamic positions
    chart_height = 150
    chart_width = min(250, (page_width - 3 * margin) // 2)
    chart_y = y - chart_height

    if stats and heatmap is not None and gray is not None:
        focus_chart = get_focus_heatmap(heatmap)
        hist_chart = get_intensity_histogram(gray)

        # Draw charts side by side
        c.drawImage(ImageReader(focus_chart), margin, chart_y, width=chart_width, height=chart_height)
        c.drawImage(ImageReader(hist_chart), margin * 2 + chart_width, chart_y, width=chart_width, height=chart_height)

        # Inference Bar (Legend) for Focus Heatmap
        legend_y = chart_y - 30
        legend_x = margin
        box_size = 15
        legend_gap = 160
        c.setFont("Helvetica-Bold", 12)
        c.drawString(legend_x, legend_y, "Focus Heatmap Legend:")

        # Red
        c.setFillColorRGB(1, 0, 0)
        c.rect(legend_x, legend_y - 20, box_size, box_size, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(legend_x + box_size + 5, legend_y - 18, "Red: Sharp/Well-focused areas")

        # Yellow
        c.setFillColorRGB(1, 1, 0)
        c.rect(legend_x + legend_gap, legend_y - 20, box_size, box_size, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(legend_x + legend_gap + box_size + 5, legend_y - 18, "Yellow: Moderately focused")

        # White
        c.setFillColorRGB(1, 1, 1)
        c.rect(legend_x + 2 * legend_gap, legend_y - 20, box_size, box_size, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(legend_x + 2 * legend_gap + box_size + 5, legend_y - 18, "White: Blurry/Bounced light")

        # Black
        c.setFillColorRGB(0, 0, 0)
        c.rect(legend_x + 3 * legend_gap, legend_y - 20, box_size, box_size, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(legend_x + 3 * legend_gap + box_size + 5, legend_y - 18, "Black: Very low focus")

        # Simple explanation for common readers
        c.setFont("Helvetica", 10)
        c.drawString(legend_x, legend_y - 45,
            "This heatmap shows which parts of the image are in focus. "
            "Red means sharp and clear, yellow is medium focus, white is blurry or light bounced, "
            "and black means very little focus. Use this to see which areas of the photo are clearest."
        )

        # Pixel Density Chart explanation
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin * 2 + chart_width, chart_y - 20, "Pixel Density Variation")
        c.setFont("Helvetica", 10)
        c.drawString(margin * 2 + chart_width, chart_y - 35, "Shows distribution of pixel brightness across the image.")

    # Add explanations page
    c.showPage()
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, page_height - margin, "Image Metrics Explained")
    c.setFont("Helvetica", 12)
    y = page_height - margin - 40

    for key in keys:
        explanation = METRIC_EXPLANATIONS.get(key, "No explanation available.")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, key + ":")
        c.setFont("Helvetica", 12)
        c.drawString(margin + 150, y, explanation)
        y -= 25
        if y < margin + 40:
            c.showPage()
            c.setFont("Helvetica-Bold", 18)
            c.drawString(margin, page_height - margin, "Image Metrics Explained (contd.)")
            c.setFont("Helvetica", 12)
            y = page_height - margin - 40

    c.showPage()

def add_metrics_explanation_page(c, stats, page_width, page_height, margin=50):
    # Extended explanations for each metric
    TECHNICAL_EXPLANATIONS = {
        "File Name": "The name of the image file.",
        "Resolution": "Width × height of the image in pixels. Higher is usually better for detail.",
        "Aspect Ratio": "Ratio of width to height. Typical ratios: 4:3, 16:9. Unusual ratios may distort images.",
        "Total Pixels": "Total number of pixels. More pixels mean higher potential detail.",
        "Megapixels": "Image size in millions of pixels. >2MP is good for prints, >8MP for professional use.",
        "Sharpness": "How clear or crisp the image is. Range: 0-100+. Above 50 is considered sharp.",
        "Noise Level": "Random variation in brightness/color. Range: 0-100+. Below 20 is good, above 40 is noisy.",
        "Contrast": "Difference between darkest and brightest parts. Range: 0-100+. 30-70 is typical.",
        "Dynamic Range": "Range of brightness levels captured. Higher is better for shadow/highlight detail.",
        "Entropy": "Amount of information/detail. Higher means more texture and features.",
        "Mean Brightness": "Average pixel brightness. Range: 0-255. 80-180 is typical.",
        "Edge Density": "How many edges/details are present. Higher means more texture, but too high can mean noise.",
        "Fully In Focus": "Whether the whole image is sharp. 'Yes' is ideal.",
        "Focus Coverage": "Percentage of the image in focus. >70% is good for most uses.",
        "Colorfulness": "How vivid/intense the colors are. Higher is more colorful.",
        "Saturation": "Intensity of colors. Range: 0-255. 80-200 is typical.",
        "White Balance Deviation": "How much color balance differs from neutral. Lower is better; high values mean color cast.",
        "Overall Quality": "Summary based on all metrics. 'Good' means most metrics are in optimal ranges."
    }

    c.showPage()
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, page_height - margin, "Image Metrics: Technical Explanation")
    y = page_height - margin - 40

    c.setFont("Helvetica", 12)
    for key in stats.keys():
        explanation = TECHNICAL_EXPLANATIONS.get(key, "No explanation available.")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, key + ":")
        c.setFont("Helvetica", 12)
        c.drawString(margin + 180, y, explanation)
        y -= 30
        if y < margin + 40:
            c.showPage()
            c.setFont("Helvetica-Bold", 20)
            c.drawString(margin, page_height - margin, "Image Metrics: Technical Explanation (contd.)")
            y = page_height - margin - 40

    c.showPage()

def run_image_analysis_pipeline(image_path, output_path):
    # This function should encompass the entire image analysis and reporting pipeline.
    # It will call all necessary functions in order, including metrics calculation,
    # image processing, and PDF report generation.

    # 1. Calculate metrics
    stats = calculate_image_metrics(image_path)

    # 2. Process images (e.g., enhance, denoise)
    processed_image_path = process_image(image_path, output_path, stats)

    # 3. Generate PDF report
    c = canvas.Canvas(output_path.replace(".jpg", "_report.pdf"), pagesize=A2)
    generate_pdf(c, image_path, processed_image_path, stats, **detected_objects)


    c.save()

    # 4. (Optional) Upload or email the report
    # upload_report(output_path.replace(".jpg", "_report.pdf"))

    # For debugging: return paths of generated files
    return {
        "original_image": image_path,
        "processed_image": processed_image_path,
        "report": output_path.replace(".jpg", "_report.pdf")
    }