import cv2
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt
import io

def analyze_quality(image, file_name="unknown", grid_size=8, focus_threshold=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    total_pixels = height * width
    megapixels = round(total_pixels / 1_000_000, 2)
    aspect_ratio = round(width / height, 2)

    global_sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    noise = np.mean(cv2.absdiff(gray, blur))
    contrast = np.std(gray)
    dynamic_range = np.max(gray) - np.min(gray)
    dynamic_range_norm = dynamic_range / 255
    entropy = measure.shannon_entropy(gray)
    mean_intensity = np.mean(gray)

    h_block, w_block = height // grid_size, width // grid_size
    sharp_blocks = 0
    total_blocks = grid_size * grid_size
    heatmap = np.zeros((grid_size, grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            y, x = i * h_block, j * w_block
            block = gray[y:y + h_block, x:x + w_block]
            block_var = cv2.Laplacian(block, cv2.CV_64F).var()
            if block_var >= focus_threshold:
                sharp_blocks += 1
            heatmap[i, j] = block_var

    focus_ratio = sharp_blocks / total_blocks
    focus_status = "Yes" if focus_ratio >= 0.8 else "Partial" if focus_ratio >= 0.5 else "No"

    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / total_pixels

    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    colorfulness = np.std(image_lab[:, :, 1]) + np.std(image_lab[:, :, 2])
    saturation = np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 1])
    avg_rgb = np.mean(image, axis=(0, 1))
    white_balance_deviation = np.std(avg_rgb)

    def rate(val, good, avg): return "Good" if val >= good else "Average" if val >= avg else "Poor"
    sharpness_level = rate(global_sharpness, 200, 100)
    noise_level = rate(-noise, -10, -20)
    contrast_level = rate(contrast, 50, 30)
    dynamic_range_level = rate(dynamic_range_norm, 0.6, 0.3)
    edge_density_level = rate(edge_density, 0.04, 0.02)
    entropy_level = rate(entropy, 6.5, 5.0)

    ratings = [
        sharpness_level, noise_level, contrast_level,
        dynamic_range_level, edge_density_level, entropy_level
    ]
    quality = "Good" if ratings.count("Good") >= 4 else "Poor" if ratings.count("Poor") >= 3 else "Average"

    stats = {
        "File Name": file_name,
        "Resolution": f"{width}×{height}",
        "Aspect Ratio": aspect_ratio,
        "Total Pixels": total_pixels,
        "Megapixels": f"{megapixels:.2f} MP",
        "Sharpness": f"{global_sharpness:.2f} ({sharpness_level})",
        "Noise Level": f"{noise:.2f} ({noise_level})",
        "Contrast": f"{contrast:.2f} ({contrast_level})",
        "Dynamic Range": f"{dynamic_range_norm:.2f} ({dynamic_range_level})",
        "Entropy": f"{entropy:.2f} ({entropy_level})",
        "Mean Brightness": f"{mean_intensity:.2f}",
        "Edge Density": f"{edge_density:.4f} ({edge_density_level})",
        "Fully In Focus": focus_status,
        "Focus Coverage": f"{focus_ratio*100:.1f}%",
        "Colorfulness": f"{colorfulness:.2f}",
        "Saturation": f"{saturation:.2f}",
        "White Balance Deviation": f"{white_balance_deviation:.2f}",
        "Overall Quality": quality
    }

    return stats, heatmap, gray

# 📊 Visualizations

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def fig_to_buf(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

def get_metrics_chart(stats):
    keys = []
    values = []
    for k in stats:
        v = str(stats[k]).split()[0]
        if is_float(v):
            keys.append(k)
            values.append(float(v))
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(keys, values, color='royalblue')
    ax.set_xticklabels(keys, rotation=45, ha='right')
    ax.set_title(f"Image Metrics: {stats['File Name']}")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()
    buf = fig_to_buf(fig)
    plt.close(fig)
    return buf

def get_focus_heatmap(heatmap):
    fig, ax = plt.subplots(figsize=(4, 3))
    im = ax.imshow(heatmap, cmap='hot', interpolation='nearest')
    fig.colorbar(im, ax=ax, label="Laplacian Variance")
    ax.set_title("Focus Sharpness Heatmap")
    ax.set_xlabel("Grid Columns")
    ax.set_ylabel("Grid Rows")
    fig.tight_layout()
    buf = fig_to_buf(fig)
    plt.close(fig)
    return buf

def get_intensity_histogram(gray):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(gray.ravel(), bins=256, range=[0,256], color='slategray')
    ax.set_title("Pixel Intensity Distribution")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    buf = fig_to_buf(fig)
    plt.close(fig)
    return buf
