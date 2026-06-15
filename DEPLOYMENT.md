# 🚀 AeroVision AI - Deployment Guide

## Cloud & Edge Deployment Options

---

## 🖥️ Option 1: Local Desktop/Server

### Windows

```bash
# 1. Clone repository
git clone https://github.com/MUGESH-KUMAR-M/AeroVision-AI.git
cd AeroVision-AI

# 2. Create virtual environment
python -m venv aerovision_env
aerovision_env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train or load model
python train.py --model yolov8s.pt --data_dir data.yaml

# 5. Start web interface
python app.py
# Open: http://localhost:5000
```

### Linux/Mac

```bash
# 1-3. Same as above
git clone https://github.com/MUGESH-KUMAR-M/AeroVision-AI.git
cd AeroVision-AI
python3 -m venv aerovision_env
source aerovision_env/bin/activate
pip install -r requirements.txt

# 4-5. Run
python train.py --model yolov8s.pt --data_dir data.yaml
python app.py
```

---

## 🤖 Option 2: NVIDIA Jetson Nano (Edge Device)

### Prerequisites
- Jetson Nano 2GB/4GB
- JetPack 4.6+
- 32GB+ microSD card

### Installation

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3-pip python3-venv libatlas-base-dev libjasper-dev
sudo apt install -y libharfbuzz0b libwebp6 libtiff5 libjasper1 libjasper-dev

# 3. Clone AeroVision
git clone https://github.com/MUGESH-KUMAR-M/AeroVision-AI.git
cd AeroVision-AI

# 4. Create virtual environment
python3 -m venv jetson_env
source jetson_env/bin/activate

# 5. Install PyTorch for Jetson
pip install numpy
sudo apt install -y libopenblas-dev libblas-dev m4 cmake
pip install --upgrade setuptools pip
pip install torch torchvision torchaudio --no-build-isolation

# 6. Install ultralytics
pip install ultralytics

# 7. Copy pre-trained ONNX model
# Transfer best.onnx from your PC to Jetson

# 8. Run inference
python aerovision_detect.py --image aircraft.jpg
```

### TensorRT Export for Jetson

```python
from ultralytics import YOLO

model = YOLO("runs/aerovision/aerovision_v1/weights/best.pt")
# Export to TensorRT format
model.export(format="engine")
```

---

## 🐳 Option 3: Docker Container

### Create Dockerfile

```dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone AeroVision
RUN git clone https://github.com/MUGESH-KUMAR-M/AeroVision-AI.git .

# Install Python packages
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
```

### Build and Run

```bash
# Build image
docker build -t aerovision-ai:latest .

# Run container
docker run -p 5000:5000 -v /path/to/NEU-DET:/app/NEU-DET aerovision-ai:latest

# Open: http://localhost:5000
```

---

## ☁️ Option 4: Cloud Deployment

### Google Colab (Free GPU)

```python
# In Colab notebook:

# 1. Install dependencies
!pip install ultralytics opencv-python flask

# 2. Clone repository
!git clone https://github.com/MUGESH-KUMAR-M/AeroVision-AI.git
%cd AeroVision-AI

# 3. Download dataset
!wget https://github.com/Marfbin/NEU-DET-with-yolov8/releases/download/NEU-DET/NEU-DET.zip
!unzip NEU-DET.zip

# 4. Train
!python train.py --model yolov8s.pt --data_dir data.yaml

# 5. Export ONNX
from ultralytics import YOLO
model = YOLO("runs/aerovision/aerovision_v1/weights/best.pt")
model.export(format="onnx")
```

### AWS EC2

```bash
# 1. Launch EC2 instance (Deep Learning AMI with GPU)
# Instance type: p3.2xlarge or g4dn.xlarge

# 2. SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Setup (same as Linux instructions above)
git clone https://github.com/MUGESH-KUMAR-M/AeroVision-AI.git
cd AeroVision-AI
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# 4. Train
python train.py --model yolov8s.pt --data_dir data.yaml

# 5. Setup Flask (Gunicorn + Nginx for production)
pip install gunicorn nginx
gunicorn app:app -w 4 -b 0.0.0.0:8000
```

### Azure

```bash
# Use Azure ML Compute Instance or Virtual Machine

# 1. Create resource group
az group create --name aerovision --location eastus

# 2. Create VM
az vm create --resource-group aerovision \
  --name aerovision-vm \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --admin-username azureuser

# 3. SSH and setup (same as Linux)
```

---

## 🎯 Production Deployment Checklist

### Pre-Deployment
- [ ] Train and validate model (mAP50 > 75%)
- [ ] Export to ONNX format
- [ ] Test inference on sample images
- [ ] Document model performance
- [ ] Create requirements.txt with pinned versions
- [ ] Test Flask app locally
- [ ] Add SSL certificates for HTTPS

### Deployment
- [ ] Set up monitoring (prometheus, grafana)
- [ ] Configure logging (ELK stack or CloudWatch)
- [ ] Setup backup for model weights
- [ ] Load balancing if needed
- [ ] Rate limiting for API
- [ ] CORS configuration
- [ ] API authentication/authorization

### Post-Deployment
- [ ] Monitor inference latency
- [ ] Track model performance metrics
- [ ] Setup alerts for anomalies
- [ ] Regular model retraining pipeline
- [ ] Version control for models
- [ ] Update documentation

---

## 📊 Performance Benchmarks

### Desktop (NVIDIA RTX 3060)
- Inference: ~15-20ms per image
- Throughput: ~50-66 images/second
- Memory: ~2GB GPU VRAM

### Jetson Nano (TensorRT)
- Inference: ~100-150ms per image
- Throughput: ~6-10 images/second
- Memory: ~2GB RAM

### Raspberry Pi 4 (ONNX)
- Inference: ~500-800ms per image
- Throughput: ~1-2 images/second
- Memory: ~1GB RAM

### CPU (Intel i7)
- Inference: ~200-300ms per image
- Throughput: ~3-5 images/second
- Memory: ~1GB RAM

---

## 🔧 Troubleshooting

### CUDA Not Available
```bash
# Check CUDA installation
nvidia-smi

# If not found, install:
# https://developer.nvidia.com/cuda-downloads
```

### Out of Memory
```python
# Reduce batch size in training
batch=8  # Instead of 16

# Use smaller model
# yolov8n.pt instead of yolov8m.pt
```

### Model File Too Large
```python
# Export with quantization
model.export(format="onnx", half=True)

# Simplify ONNX
pip install onnxruntime onnx-simplifier
```

---

## 📞 Support

For deployment issues:
1. Check GitHub issues: https://github.com/MUGESH-KUMAR-M/AeroVision-AI/issues
2. Review Ultralytics docs: https://docs.ultralytics.com
3. Check Flask docs: https://flask.palletsprojects.com

---

**AeroVision AI - Enterprise Aircraft Defect Detection 🛩️**
