import numpy as np
from flask import Flask, request, jsonify, render_template
from model.inference import predictClass
from PIL import Image

# Create flask app
app = Flask(__name__)



@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/predict", methods = ["POST"])
def predict():
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    if file:
        image = Image.open(file.stream)
        result = predictClass(image)
        predicted_labels = result["predictedClass"]
        if predicted_labels == 1:
            predicted_class_img = "Real Image"
        elif predicted_labels == 0:
            predicted_class_img = "AI Generated Image"
        
        return render_template("index.html", prediction_class=predicted_class_img, predicted_probabilities=result["prob"].tolist())

if __name__ == "__main__":
    app.run(debug=True)