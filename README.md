# ✈️ AeroVision AI - Aircraft Surface Defect Detection

**Edge AI-Powered Aircraft Defect Detection using YOLOv8**

Built for Tata Technologies InnoVent 2026 | Aerospace Vertical

## Overview

Traditional aircraft inspection mainly relies on manual visual inspection or basic machine vision systems, but these methods have problems such as low efficiency, low accuracy, high labor intensity, and susceptibility to human factors. AeroVision AI is an AI-powered solution for automated aircraft surface defect detection using improved YOLOv8 algorithm.
## Features

✅ **AI-Powered Detection:**
- Detects 6 aircraft defect types: crack, corrosion, scratch, surface wear, inclusion, delamination
- Real-time YOLOv8 inference — no cloud needed (edge deployment ready)
- 79.2% mAP50 on NEU-DET dataset

✅ **Multiple Deployment Options:**
- Flask web dashboard for easy access
- Python CLI for batch processing
- ONNX export for edge devices (Jetson Nano, Raspberry Pi)
- TensorRT export for NVIDIA hardware acceleration

✅ **Easy to Use:**
- Drag-and-drop web interface
- REST API endpoints
- Command-line tools for automation
- Detailed defect analysis with confidence scores

## Method

AeroVision AI uses an **improved YOLOv8 algorithm** with the following enhancements:

1. **ResCBAM Attention Mechanism** - Residual connection with CBAM for better feature extraction and reduced overfitting
2. **GhostConv Replacement** - Lightweight convolutions in backbone for efficiency without sacrificing performance
3. **WIOU Loss Function** - Improved loss function to prevent small targets from dominating and handle imbalanced data

The model has been extensively tested and deployed. For more details on the architecture and technical approach, see the sections below.

## Architecture
<p align="center">
  <img src="imgs/模型结构.jpg" width="1024" title="details"> 
</p>

### ResCBAM block
<p align="left">
  <img src="imgs/ResCBAM.jpg" width="300"> 
</p>

## Table : Comparisons with other detection models on the NEU-DET dataset models
|     Model     | Test Size |  Param.   |   FLOPs   | mAP<sub>50</sub><sup>val</sup> | mAP<sub>50-95</sub><sup>val</sup> |
| :-----------: | :-------: | :-------: | :-------: | :----------------------------: | :-------------------------------: |
|    YOLOv5s    |    640    |   7.04M   |   15.9G   |             70.87%             |              35.02%               |
|    YOLOv5m    |    640    |  20.89M   |  183.5G   |             71.74%             |              36.67%               |
|    YOLOv5l    |    640    |  46.17M   |  183.5G   |             72.23%             |              36.74%               |
|    YOLOv7     |    640    |  37.22M   |  196.2G   |             71.92%             |               37.2%               |
|    YOLOv8     |    640    |   3.01M   |   8.1G    |             77.7%              |               46.2%               |
| **Our model** |  **640**  | **4.05M** | **10.2G** |           **79.2%**            |              **47%**              |

## Figure: Comparison of accuracy before and after improvement
<p align="center">
  <img src="imgs/compare.jpg" width="1024" title="compare">
</p>

## Ablation study 
|     Model     | Test Size |  Param.   |   FLOPs   | mAP<sub>50</sub><sup>val</sup> |
| :-----------: | :-------: | :-------: | :-------: | :----------------------------: |
|    YOLOv8     |    640    |   3.01M   |   8.1G    |             77.7%              |
|    YOLOv8+GhostConv    |    640    |   2.8M   |   7.8G   |             78.7%             |
|    YOLOv8+ResCBAM    |    640    |  4.24M   |  10.5G   |             78.2%            |
| **YOLOv8+ResCBAM+GhostConv(Our)** |  **640**  | **4.05M** | **10.2G** |           **79.2%**            |

## Heatmap
<p align="center">
  <img src="imgs/heatmap.png" width="1024" title="heatmap">
</p>

## Model metrics

### PR_Curve
<p align="center">
  <img src="imgs/PR_curve.png" width="1024">
</p>

### confusion__matrix_normalized
<p align="center">
  <img src="imgs/confusion_matrix_normalized.png" width="1024">
</p>

## Results

<p align="center">
  <img src="imgs/val_labels.jpg" width="400">
  <img src="imgs/val_pred.jpg" width="400">
  <p align="center">Ground Truth (left) vs Predictions (right)</p>
</p>

---

## Project Structure

```
AeroVision-AI/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── data.yaml                          # Dataset configuration (6 defect classes)
├── train.py                           # Training script
├── aerovision_detect.py               # Inference script
├── app.py                             # Flask web application (port 5000)
├── templates/
│   ├── index.html                     # Upload & analysis interface
│   └── result.html                    # Results display page
├── static/
│   ├── uploads/                       # Uploaded images
│   └── results/                       # Detection results
├── runs/aerovision/                   # Trained model checkpoints
│   └── aerovision_v1/weights/best.pt  # Best model weights
├── NEU-DET/                           # Dataset
│   ├── train/images/
│   ├── val/images/
│   └── test/images/
├── ultralytics/                       # YOLOv8 framework
└── imgs/                              # Documentation images
```

## API Endpoints

### Flask Web API

```
POST /upload
  Upload and analyze aircraft image
  Input: multipart/form-data (image file)
  Returns: JSON with detection results

GET /api/model-info
  Get model information and class list
  Returns: {status, model, classes, model_path}

GET /api/stats
  Get application statistics
  Returns: {uploads, results, model_loaded}

GET /health
  Service health check
  Returns: {status, model_loaded, app}
```

## Export for Edge Deployment

### ONNX Export (Universal)

```python
from ultralytics import YOLO

model = YOLO("runs/aerovision/aerovision_v1/weights/best.pt")
model.export(format="onnx")  # → best.onnx
```

### TensorRT Export (Jetson Nano)

```python
model.export(format="engine")  # → best.engine
```

## Usage Examples

### Web Interface

1. Run `python app.py`
2. Navigate to http://localhost:5000
3. Upload or drag-drop aircraft image
4. View detection results with color-coded defects
5. Download annotated image

### Command Line Detection

```bash
# Single image analysis
python aerovision_detect.py --image test_aircraft.jpg

# Batch directory processing
python aerovision_detect.py --dir ./aircraft_images

# Custom model path
python aerovision_detect.py --image photo.jpg --model custom_model.pt
```

### Python Integration

```python
from aerovision_detect import inspect_image, batch_analyze

# Single image
result = inspect_image("aircraft.jpg")
print(f"Defects found: {result['count']}")
for defect in result['defects']:
    print(f"  - {defect['class']}: {defect['confidence']:.2%}")

# Batch processing
image_list = ["aircraft_1.jpg", "aircraft_2.jpg", "aircraft_3.jpg"]
results, summary = batch_analyze(image_list)
print(f"Total defects: {sum(summary.values())}")
```

### REST API Integration

```bash
# Upload image via API
curl -X POST -F "image=@aircraft.jpg" http://localhost:5000/upload

# Get model info
curl http://localhost:5000/api/model-info

# Get statistics
curl http://localhost:5000/api/stats
```

## Defect Color Legend

| Color | Defect Type | Description |
|-------|-----------|-------------|
| 🔴 Red | Crack | Surface cracks/fractures |
| 🟠 Orange | Corrosion | Corrosion/coating damage |
| 🟡 Yellow | Scratch | Surface scratches |
| 🟢 Cyan | Surface Wear | Surface erosion/wear marks |
| 🟣 Magenta | Inclusion | Foreign material inclusions |
| 🟤 Purple | Delamination | Material layer separation |

## Troubleshooting

### Model Not Loading

```
Error: Model not found
Solution: Train the model first using: python train.py --model yolov8s.pt --data_dir data.yaml
```

### CUDA/GPU Issues

```
Error: CUDA out of memory
Solutions:
  - Reduce batch size in training
  - Use smaller model (yolov8n.pt instead of yolov8m.pt)
  - Use CPU-only: os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

### Flask Port Already in Use

```
Error: Address already in use
Solution: Change port in app.py or kill process: lsof -ti:5000 | xargs kill -9
```

## Performance Metrics

```
Precision Improvement: +5.6% vs YOLOv8
F1-Score Improvement: +3.1% vs YOLOv8
mAP50 Improvement: +1.5% vs YOLOv8
Final mAP50: 79.2%
```

## Contributors

Built with ❤️ by **MUGESH KUMAR M** for **Tata Technologies InnoVent 2026**

## Citation

If you use AeroVision AI in your research or project, please cite:

```bibtex
@software{aerovision2026,
  title={AeroVision AI: Aircraft Surface Defect Detection},
  author={MUGESH KUMAR M},
  year={2026},
  url={https://github.com/MUGESH-KUMAR-M/AeroVision-AI}
}
```

## Acknowledgments

- **YOLOv8 Framework** - [Ultralytics](https://github.com/ultralytics/ultralytics)
- **NEU-DET Dataset** - Northeastern University
- **Improved Architecture** - Based on [YOLOv8_Imporved-Defect_detection](https://github.com/LZY-233/yolov8_Imporved-Defect_detection) by LZY-233
- **Original Research** - ResCBAM, GhostConv, WIOU Loss references

## License

MIT License - See LICENSE file for details

## Support & Feedback

For issues, questions, or feature requests, please open an issue on GitHub.

---

**AeroVision AI - Making Aircraft Inspection Smarter 🛩️✨**

## Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA 11.8+ (for GPU training, optional)
- 4GB+ RAM (8GB+ recommended)
- GPU recommended for training (CPU-only inference works)
- Linux (Ubuntu) or Windows 


## Dataset

### NEU-DET - Surface Defect Dataset

AeroVision AI uses the **NEU-DET** dataset - a publicly available industrial surface defect detection dataset with 6 defect classes:

- **Crazing** → Mapped to Aircraft **Crack**
- **Inclusion** → Mapped to **Inclusion**
- **Patches** → Mapped to Aircraft **Corrosion**
- **Pitted Surface** → Mapped to **Surface Wear**
- **Rolled-in Scale** → Mapped to **Delamination**
- **Scratches** → Mapped to **Scratch**

**Download Dataset:**
- Option 1: Baidu Drive: https://pan.baidu.com/s/1K-mTgSJfhFrcVSO8MUqHbQ?pwd=6666
- Option 2: GitHub: https://github.com/Marfbin/NEU-DET-with-yolov8

**Dataset Structure** (80-10-10 split):
```
NEU-DET/
├── train/images/  (80%)
├── val/images/    (10%)
└── test/images/   (10%)
```

## Quick Start

### Step 1: Clone & Setup

```bash
git clone https://github.com/MUGESH-KUMAR-M/AeroVision-AI.git
cd AeroVision-AI

# Create virtual environment
python -m venv aerovision_env
source aerovision_env/Scripts/activate  # Windows: aerovision_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download Dataset

```bash
# Download NEU-DET dataset and extract to project directory
# Resulting structure should be:
AeroVision-AI/
├── NEU-DET/
│   ├── train/images/
│   ├── val/images/
│   └── test/images/
├── app.py
├── train.py
└── data.yaml
```

### Step 3: Train Model

```bash
# Method 1: Using provided train.py
python train.py --model yolov8s.pt --data_dir data.yaml

# Method 2: Direct with ultralytics
from ultralytics import YOLO
model = YOLO("yolov8s.pt")
model.train(data="data.yaml", epochs=100, imgsz=640, batch=16)
```

### Step 4: Run Web Interface

```bash
python app.py
# Navigate to: http://localhost:5000
```

### Step 5: Run Detection

```bash
# Single image
python aerovision_detect.py --image aircraft.jpg

# Batch processing
python aerovision_detect.py --dir ./aircraft_images
```