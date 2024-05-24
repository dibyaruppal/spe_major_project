import numpy as np
from flask import Flask, request, jsonify, render_template
from inference import predictClass
from PIL import Image
import logging
from kubernetes import client, config
import threading
from flask_cors import CORS
from kubernetes.client.rest import ApiException
import subprocess
from logging.handlers import RotatingFileHandler

# Create flask app
app = Flask(__name__)
CORS(app)

# Configure logging to store logs in a file
handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Define the dataset path
DATASET_DIR = "/mnt/data/ai_images_vs_real_images"

# Function to check if the uploaded file is an allowed image type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def trigger_training_job(namespace, pod_name, container_name, command):
    config.load_incluster_config()  # Load Kubernetes config for in-cluster access

    api_instance = client.CoreV1Api()

    try:
        resp = api_instance.connect_get_namespaced_pod_exec(
            name=pod_name,
            namespace=namespace,
            command=["/bin/sh", "-c", command],
            container=container_name,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False,
            _preload_content=False,
        )
        return resp.read_stream()

    except ApiException as e:
        return f"Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: {e}\n"

def trigger_training_in_thread():
    namespace = "default" 
    pod_name = "train-pod"  
    container_name = "train-container"  
    command = "python train.py"  

    result = trigger_training_job(namespace, pod_name, container_name, command)
    app.logger.info(result)

@app.route("/predict", methods=["POST"])
def predict():
    app.logger.info('Prediction request received')
    if 'image' not in request.files:
        app.logger.error('No file part')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        app.logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            app.logger.info('Processing uploaded image')
            image = Image.open(file.stream)
            result = predictClass(image)
            predicted_labels = result["predictedClass"]
            predicted_class_img = "Real Image" if predicted_labels == 1 else "AI Generated Image"
            app.logger.info('Prediction successful')
            # Trigger training in a separate thread to ensure non-blocking
            training_thread = threading.Thread(target=trigger_training_in_thread)
            training_thread.start()
            return jsonify({
                'prediction_class': predicted_class_img,
                'predicted_probabilities': result["prob"].tolist()
            })
        except Exception as e:
            app.logger.error(f'Error during prediction: {e}')
            return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500
    else:
        app.logger.error('Allowed image types are: png, jpg, jpeg')
        return jsonify({'error': 'Allowed image types are: png, jpg, jpeg'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
