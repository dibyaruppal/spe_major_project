import numpy as np
from flask import Flask, request, jsonify, render_template
from inference import predictClass
from PIL import Image
import logging

# Create flask app
app = Flask(__name__)

# Configure logging to store logs in a file
logging.basicConfig(filename='flask_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if the uploaded file is an allowed image type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/predict", methods=["POST"])
def predict():
    logging.info('Prediction request received')
    if 'image' not in request.files:
        logging.error('No file part')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            logging.info('Processing uploaded image')
            image = Image.open(file.stream)
            result = predictClass(image)
            predicted_labels = result["predictedClass"]
            predicted_class_img = "Real Image" if predicted_labels == 1 else "AI Generated Image"
            logging.info('Prediction successful')
            return jsonify({
                'prediction_class': predicted_class_img,
                'predicted_probabilities': result["prob"].tolist()
            })
        except Exception as e:
            logging.error(f'Error during prediction: {e}')
            return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500
    else:
        logging.error('Allowed image types are: png, jpg, jpeg')
        return jsonify({'error': 'Allowed image types are: png, jpg, jpeg'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')