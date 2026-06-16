"""
AeroVision AI - Export trained model for edge deployment (ONNX / TensorRT).
"""

import argparse
from pathlib import Path

from ultralytics import YOLO

DEFAULT_WEIGHTS = "runs/train1/weights/best.pt"


def parse_args():
    parser = argparse.ArgumentParser(description="Export AeroVision model for deployment")
    parser.add_argument("--weights", type=str, default=DEFAULT_WEIGHTS, help="Path to best.pt")
    parser.add_argument(
        "--format",
        type=str,
        default="onnx",
        choices=["onnx", "engine", "tflite", "torchscript"],
        help="Export format",
    )
    parser.add_argument("--imgsz", type=int, default=640)
    return parser.parse_args()


def main():
    args = parse_args()
    weights = Path(args.weights)

    if not weights.exists():
        raise FileNotFoundError(
            f"Model weights not found: {weights}\n"
            "Train first: python train.py --model yolov8s.pt --data_dir data.yaml"
        )

    print(f"Exporting {weights} -> {args.format}")
    model = YOLO(str(weights))
    out = model.export(format=args.format, imgsz=args.imgsz)
    print(f"Export saved: {out}")


if __name__ == "__main__":
    main()
