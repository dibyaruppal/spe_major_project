import numpy as np
from flask import Flask, request, jsonify, render_template
from inference import predictClass
from PIL import Image
import logging
from kubernetes import client, config
import threading
from flask_cors import CORS

# Create flask app
app = Flask(__name__)
CORS(app)

# Configure logging to store logs in a file
logging.basicConfig(filename='flask_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Define the dataset path
DATASET_DIR = "/mnt/data/ai_images_vs_real_images"

# Function to check if the uploaded file is an allowed image type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def trigger_training_job():
    # Load kube config from default location
    config.load_kube_config()

    # Create a Kubernetes API client
    batch_v1 = client.BatchV1Api()

    # Define the Job object
    job_name = "train-job-template"
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name)
    )

    # Define the container spec
    container = client.V1Container(
        name="train",
        image="rahulb2180/spe_major_project_model",
        command=["python", "train.py"],
        volume_mounts=[client.V1VolumeMount(mount_path="/mnt/data", name="model-storage")]
    )

    # Define the pod template spec
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "train"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]),
    )

    job.spec = client.V1JobSpec(template=template, volumes=[client.V1Volume(name="model-storage", host_path=client.V1HostPathVolumeSource(path="/mnt/data"))])

    # Create the Job in the Kubernetes cluster
    batch_v1.create_namespaced_job(namespace="default", body=job)


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
             # Trigger training in a separate thread to ensure non-blocking
            training_thread = threading.Thread(target=trigger_training_job)
            training_thread.start()
            return jsonify({
                'prediction_class': predicted_class_img,
                'predicted_probabilities': result["prob"].tolist()
            })
        except Exception as e:
            print(e)
            logging.error(f'Error during prediction: {e}')
            return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500
    else:
        logging.error('Allowed image types are: png, jpg, jpeg')
        return jsonify({'error': 'Allowed image types are: png, jpg, jpeg'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')