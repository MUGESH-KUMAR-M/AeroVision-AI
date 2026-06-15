#!/bin/bash
# AeroVision AI - Quick Start Script
# Run this script to set up AeroVision AI on your system

echo "🛩️  AeroVision AI - Quick Start Setup"
echo "====================================="

# Step 1: Create virtual environment
echo ""
echo "1️⃣ Creating virtual environment..."
python -m venv aerovision_env
source aerovision_env/Scripts/activate  # Windows: aerovision_env\Scripts\activate

# Step 2: Install dependencies
echo ""
echo "2️⃣ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Verify installation
echo ""
echo "3️⃣ Verifying installation..."
python -c "from ultralytics import YOLO; print('✅ Ultralytics installed')"
python -c "import cv2; print('✅ OpenCV installed')"
python -c "import flask; print('✅ Flask installed')"

# Step 4: Download dataset info
echo ""
echo "4️⃣ Dataset Information:"
echo "   Download NEU-DET from:"
echo "   - GitHub: https://github.com/Marfbin/NEU-DET-with-yolov8"
echo "   - Baidu: https://pan.baidu.com/s/1K-mTgSJfhFrcVSO8MUqHbQ?pwd=6666"
echo ""
echo "   Extract to: ./NEU-DET/"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Download and extract NEU-DET dataset"
echo "  2. Train model: python train.py --model yolov8s.pt --data_dir data.yaml"
echo "  3. Start web UI: python app.py"
echo "  4. Open: http://localhost:5000"
