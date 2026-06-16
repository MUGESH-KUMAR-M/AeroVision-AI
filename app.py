"""
AeroVision AI - Flask Web Dashboard
Web interface for aircraft defect detection
"""

import os
import uuid
import cv2
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify
from ultralytics import YOLO
from werkzeug.utils import secure_filename


# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'bmp'}

# Create folders
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path('static/results').mkdir(parents=True, exist_ok=True)

# Load model — check common training output locations
MODEL_CANDIDATES = [
    "runs/aerovision/aerovision_v1/weights/best.pt",
    "runs/train1/weights/best.pt",
    "runs/train1/weights/last.pt",
    "runs/train/weights/best.pt",
    "runs/train/weights/last.pt",
]

MODEL_PATH = next((p for p in MODEL_CANDIDATES if os.path.exists(p)), MODEL_CANDIDATES[0])
if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
    print(f"[OK] Model loaded: {MODEL_PATH}")
else:
    model = None
    print("[WARN] Model not found. Train model first: python train.py")

# Defect color mapping
DEFECT_COLORS = {
    "crack":        (0, 0, 255),
    "corrosion":    (0, 165, 255),
    "scratch":      (255, 255, 0),
    "surface_wear": (0, 255, 255),
    "inclusion":    (255, 0, 255),
    "delamination": (255, 100, 0),
}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def process_image(image_path):
    """
    Run detection on image and return annotated result
    """
    if not model:
        return None, "Model not loaded. Please train the model first."
    
    try:
        # Run inference
        results = model(image_path, conf=0.25)[0]
        
        # Read image
        img = cv2.imread(image_path)
        defects_list = []
        
        # Draw results
        for box in results.boxes:
            cls_id = int(box.cls)
            cls_name = model.names[cls_id]
            conf = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = DEFECT_COLORS.get(cls_name, (255, 255, 255))
            
            # Bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            
            # Label
            label = f"{cls_name} {conf:.1%}"
            cv2.putText(img, label, (x1, y1 - 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            defects_list.append({
                "type": cls_name,
                "confidence": f"{conf:.1%}"
            })
        
        # Save result
        output_filename = f"result_{uuid.uuid4().hex}.jpg"
        output_path = os.path.join('static/results', output_filename)
        cv2.imwrite(output_path, img)
        
        return {
            "image": output_path,
            "defects": defects_list,
            "count": len(defects_list)
        }, None
    
    except Exception as e:
        return None, f"Error processing image: {str(e)}"


@app.route('/')
def index():
    """Home page - upload interface"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and detection"""
    if not model:
        return jsonify({
            'error': 'Model not loaded. Training is still in progress — wait for best.pt, then restart the app.'
        }), 503

    # Check if file present
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use JPG, PNG, or BMP'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process image
        result, error = process_image(filepath)
        
        if error:
            code = 503 if not model else 500
            return jsonify({'error': error}), code
        
        return jsonify({
            'success': True,
            'result': result,
            'message': f"Detection complete! Found {result['count']} defect(s)."
        })
    
    except Exception as e:
        return jsonify({'error': f"Upload failed: {str(e)}"}), 500


@app.route('/api/model-info')
def model_info():
    """Get model information"""
    if not model:
        return jsonify({
            'status': 'not-loaded',
            'message': 'Model not trained yet'
        })
    
    return jsonify({
        'status': 'loaded',
        'model': 'YOLOv8 (Improved)',
        'classes': list(model.names.values()),
        'model_path': MODEL_PATH
    })


@app.route('/api/stats')
def get_stats():
    """Get application statistics"""
    upload_count = len(os.listdir(app.config['UPLOAD_FOLDER'])) if os.path.exists(app.config['UPLOAD_FOLDER']) else 0
    result_count = len(os.listdir('static/results')) if os.path.exists('static/results') else 0
    
    return jsonify({
        'uploads': upload_count,
        'results': result_count,
        'model_loaded': model is not None
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'app': 'AeroVision AI'
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large"""
    return jsonify({'error': 'File too large. Maximum size: 16MB'}), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("   AeroVision AI - Aircraft Defect Detection")
    print("="*60)
    print("\nStarting Flask web server...")
    print("   Open: http://localhost:5000")
    print("   Stop: Ctrl+C")
    print("\n" + "="*60 + "\n")
    
    # Run development server
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
