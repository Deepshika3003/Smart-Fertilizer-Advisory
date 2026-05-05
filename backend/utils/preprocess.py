import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# -----------------------------------------
# Preprocess image for prediction
# -----------------------------------------
def preprocess_image(image_file):

    # Open image
    img = Image.open(image_file)

    # Convert to RGB (in case image is RGBA / grayscale)
    img = img.convert('RGB')

    # Resize to model input size
    img = img.resize((224, 224))

    # Convert to numpy array
    img_array = np.array(img)

    # IMPORTANT: Must match training preprocessing
    img_array = preprocess_input(img_array)

    # Add batch dimension (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


# -----------------------------------------
# Convert model prediction to label + confidence
# -----------------------------------------
def get_prediction_label(prediction):

    # Class order MUST match training generator
    classes = [
        'healthy',
        'nitrogen',
        'phosphorus',
        'potassium'
    ]

    # Get highest probability index
    predicted_index = np.argmax(prediction)

    # Confidence percentage
    confidence = float(np.max(prediction) * 100)

    # Map to class label
    label = classes[predicted_index]
    print("Predicted index:", predicted_index)
    print("Predicted label:", label)
    return label, confidence