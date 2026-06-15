"""
AeroVision AI - Aircraft Defect Detection Inference
Standalone detection script for analyzing aircraft surface defects
"""

import cv2
import os
from pathlib import Path
from ultralytics import YOLO


# Color map for different defect types
DEFECT_COLORS = {
    "crack":        (0, 0, 255),       # Red
    "corrosion":    (0, 165, 255),     # Orange
    "scratch":      (255, 255, 0),     # Cyan
    "surface_wear": (0, 255, 255),     # Yellow
    "inclusion":    (255, 0, 255),     # Magenta
    "delamination": (255, 100, 0),     # Purple
}


def inspect_image(image_path, model_path=None):
    """
    Run defect detection on a single image
    
    Args:
        image_path: Path to aircraft image
        model_path: Path to trained model weights
    
    Returns:
        Dictionary with results: defects, count, confidence scores
    """
    if model_path is None:
        model_path = "runs/aerovision/aerovision_v1/weights/best.pt"
    
    # Load model
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        print(f"   Make sure to train the model first using train.py")
        return None
    
    model = YOLO(model_path)
    
    # Run inference
    print(f"🔍 Analyzing: {image_path}")
    results = model(image_path, conf=0.25)[0]
    
    # Draw results on image
    img = results.orig_img.copy()
    defects_found = []
    
    for box in results.boxes:
        cls_id = int(box.cls)
        cls_name = model.names[cls_id]
        conf = float(box.conf)
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        color = DEFECT_COLORS.get(cls_name, (255, 255, 255))
        
        # Draw bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
        # Draw label with confidence
        label = f"{cls_name} {conf:.2%}"
        cv2.putText(img, label, (x1, y1 - 8), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        defects_found.append({
            "class": cls_name,
            "confidence": conf,
            "bbox": (x1, y1, x2, y2)
        })
    
    # Save result image
    output_path = str(image_path).replace(".jpg", "_detected.jpg").replace(".png", "_detected.png")
    cv2.imwrite(output_path, img)
    print(f"✅ Saved result: {output_path}")
    
    # Display
    print(f"\n📊 Detection Results:")
    print(f"   Total Defects: {len(defects_found)}")
    for defect in defects_found:
        print(f"   - {defect['class']}: {defect['confidence']:.2%} confidence")
    
    return {
        "image_path": image_path,
        "output_path": output_path,
        "defects": defects_found,
        "count": len(defects_found),
        "img_array": img
    }


def inspect_directory(dir_path, model_path=None, output_dir="./detections"):
    """
    Run defect detection on all images in a directory
    
    Args:
        dir_path: Directory containing images
        model_path: Path to trained model
        output_dir: Where to save results
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(Path(dir_path).glob(f"*{ext}"))
    
    print(f"🎯 Found {len(image_files)} images in {dir_path}")
    
    results = []
    for img_file in image_files:
        result = inspect_image(str(img_file), model_path)
        if result:
            results.append(result)
    
    return results


def batch_analyze(image_list, model_path=None):
    """
    Analyze multiple images and return summary statistics
    """
    results = []
    defect_summary = {}
    
    for img_path in image_list:
        result = inspect_image(img_path, model_path)
        if result:
            results.append(result)
            
            # Aggregate statistics
            for defect in result['defects']:
                cls_name = defect['class']
                if cls_name not in defect_summary:
                    defect_summary[cls_name] = 0
                defect_summary[cls_name] += 1
    
    print("\n📈 Summary Statistics:")
    print(f"   Total Images Analyzed: {len(results)}")
    print(f"   Total Defects Found: {sum(r['count'] for r in results)}")
    print("   Defect Breakdown:")
    for defect_type, count in defect_summary.items():
        print(f"      - {defect_type}: {count}")
    
    return results, defect_summary


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AeroVision AI - Aircraft Defect Detection"
    )
    parser.add_argument("--image", type=str, help="Path to image file")
    parser.add_argument("--dir", type=str, help="Path to directory with images")
    parser.add_argument("--model", type=str, 
                       default="runs/aerovision/aerovision_v1/weights/best.pt",
                       help="Path to model weights")
    
    args = parser.parse_args()
    
    if args.image:
        inspect_image(args.image, args.model)
    elif args.dir:
        inspect_directory(args.dir, args.model)
    else:
        print("Usage: python aerovision_detect.py --image <path> [--model <path>]")
        print("   or: python aerovision_detect.py --dir <path> [--model <path>]")
