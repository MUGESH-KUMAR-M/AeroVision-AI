"""
AeroVision AI - Model Training Script
Trains improved YOLOv8 (ResCBAM + GhostConv) on NEU-DET aircraft defect classes.
"""

import argparse
import configparser
from pathlib import Path

import yaml
from ultralytics import YOLO

IMPROVED_MODEL = "ultralytics/cfg/models/v8/yolov8_ResBlock_CBAM_GhostConv.yaml"
DEFAULT_DATA = "data.yaml"
DEFAULT_PRETRAINED = "yolov8s.pt"


def _ini_value(raw: str):
    """Strip inline comments from config.ini values."""
    return raw.split("#", 1)[0].strip()


def load_config():
    """Load optional settings from config.ini."""
    cfg = {
        "epochs": 100,
        "batch": 16,
        "imgsz": 640,
        "device": None,
        "amp": False,
        "workers": 2,
        "patience": 20,
        "project": "runs/aerovision",
        "name": "aerovision_v1",
    }
    ini_path = Path("config.ini")
    if not ini_path.exists():
        return cfg

    parser = configparser.ConfigParser()
    parser.read(ini_path)

    if parser.has_section("training"):
        section = parser["training"]
        cfg["epochs"] = int(_ini_value(section.get("epochs", str(cfg["epochs"]))))
        cfg["batch"] = int(_ini_value(section.get("batch_size", str(cfg["batch"]))))
        cfg["imgsz"] = int(_ini_value(section.get("image_size", str(cfg["imgsz"]))))
        device = _ini_value(section.get("device", ""))
        cfg["device"] = device if device else None
        cfg["amp"] = _ini_value(section.get("amp", str(cfg["amp"]))).lower() in {"1", "true", "yes"}
        cfg["patience"] = int(_ini_value(section.get("patience", str(cfg["patience"]))))

    return cfg


def parse_args():
    defaults = load_config()
    parser = argparse.ArgumentParser(description="AeroVision AI - Train defect detection model")
    parser.add_argument(
        "--model",
        type=str,
        default=IMPROVED_MODEL,
        help="Model YAML or .pt path (default: improved YOLOv8 architecture)",
    )
    parser.add_argument("--data_dir", type=str, default=DEFAULT_DATA, help="Path to data.yaml")
    parser.add_argument("--pretrained", type=str, default=DEFAULT_PRETRAINED, help="Pretrained weights for transfer learning")
    parser.add_argument("--epochs", type=int, default=defaults["epochs"])
    parser.add_argument("--batch", type=int, default=defaults["batch"])
    parser.add_argument("--imgsz", type=int, default=defaults["imgsz"])
    parser.add_argument("--device", type=str, default=defaults["device"])
    parser.add_argument("--workers", type=int, default=defaults["workers"])
    parser.add_argument("--project", type=str, default=defaults["project"])
    parser.add_argument("--name", type=str, default=defaults["name"])
    return parser.parse_args()


def resolve_data_yaml(data_yaml: str) -> str:
    """Resolve dataset paths relative to project root for Ultralytics."""
    data_path = Path(data_yaml).resolve()
    project_root = data_path.parent

    with open(data_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    dataset_path = Path(data.get("path", "."))
    if not dataset_path.is_absolute():
        dataset_path = (project_root / dataset_path).resolve()

    data["path"] = str(dataset_path)

    resolved_yaml = project_root / "_data_resolved.yaml"
    with open(resolved_yaml, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    return str(resolved_yaml)


def build_model(model_path: str, pretrained: str):
    """Load improved architecture or existing checkpoint."""
    if model_path.endswith((".yaml", ".yml")):
        model = YOLO(model_path)
        if pretrained and Path(pretrained).exists():
            model.load(pretrained)
        elif pretrained:
            # Downloads official YOLOv8 weights when missing locally
            model.load(pretrained)
        return model
    return YOLO(model_path)


def main():
    args = parse_args()

    if not Path(args.data_dir).exists():
        raise FileNotFoundError(
            f"Dataset config not found: {args.data_dir}\n"
            "Run: python download_dataset.py"
        )

    dataset_root = Path("./NEU-DET")
    if not dataset_root.exists():
        raise FileNotFoundError(
            "NEU-DET dataset folder not found.\n"
            "Run: python download_dataset.py"
        )

    print("=" * 60)
    print("  AeroVision AI - Training")
    print("=" * 60)
    print(f"  Model:      {args.model}")
    print(f"  Data:       {args.data_dir}")
    print(f"  Epochs:     {args.epochs}")
    print(f"  Batch:      {args.batch}")
    print(f"  Image size: {args.imgsz}")
    print(f"  Output:     {args.project}/{args.name}")
    print("=" * 60)

    model = build_model(args.model, args.pretrained)
    resolved_data = resolve_data_yaml(args.data_dir)
    train_kwargs = {
        "data": resolved_data,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "name": args.name,
        "project": args.project,
        "amp": False,
        "workers": args.workers,
        "patience": load_config()["patience"],
    }
    if args.device is not None:
        train_kwargs["device"] = args.device

    model.train(**train_kwargs)
    print(f"\nTraining complete. Best weights: {args.project}/{args.name}/weights/best.pt")


if __name__ == "__main__":
    main()
