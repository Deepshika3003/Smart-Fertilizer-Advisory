from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from preprocess import preprocess_image, get_prediction_label
from recommendation import get_recommendation

app = Flask(__name__)
CORS(app)


# ============================================
# Load Models
# ============================================

print("Loading models...")

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'models')

# Load Rice Model
#rice_model_path = os.path.join(MODELS_DIR, 'rice_model.h5')
#print("Loading Rice Model From:", rice_model_path)
#rice_model = tf.keras.models.load_model(rice_model_path)
#print("Rice model loaded! ✅")

# Load Corn Model


print("All models loaded! ✅")

# ============================================
# API Endpoints
# ============================================

# Home endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "NPK Fertilizer Advisory System API",
        "status": "running",
        "crops": ["rice"]
    })

# Predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
       # rice_model_path = os.path.join(MODELS_DIR, 'rice_model.h5')
        #rice_model = tf.keras.models.load_model(rice_model_path)
        # Get inputs
        crop = request.form.get('crop').lower()
        days = int(request.form.get('days'))
        image = request.files.get('image')

        # Validate inputs
        if not crop or not days or not image:
            return jsonify({
                "error": "Please provide crop, days and image"
            }), 400

        if crop not in ['rice']:
            return jsonify({
                "error": "Crop must be rice"
            }), 400
        return jsonify({
    "message": "API working"
            })

        # Preprocess image
        img_array = preprocess_image(image)

        # Select correct model
        if crop == 'rice':
            model = rice_model
        

        # Get prediction
        prediction = model.predict(img_array)
        print("Prediction array:", prediction)
        print("Predicted index:", np.argmax(prediction))   # 👈 ADD HERE

        # Get label and confidence
        label, confidence = get_prediction_label(prediction)

        # Get recommendation
        recommendation = get_recommendation(crop, days, label)

        # Build response (growth_stage removed)
        response = {
            "success"     : True,
            "crop"        : crop,
            "days"        : days,
            "deficiency"  : label,
            "confidence"  : round(confidence, 2),
            "fertilizer"  : recommendation["fertilizer"],
            "dosage"      : recommendation["dosage"],
            "method"      : recommendation["method"],
            "npk_tip"     : recommendation["npk_tip"],
            "npk_status"  : recommendation["npk_status"],
            "cost_saving" : recommendation["cost_saving"]
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Get supported crops
@app.route('/crops', methods=['GET'])
def get_crops():
    return jsonify({
        "crops": ["rice"]
    })
@app.route('/test')
def test():
    return jsonify({
        "message": "Prediction API working"
    })
# ============================================
# Run App
# ============================================

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)