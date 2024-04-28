import numpy as np
from flask import Flask, request, jsonify, render_template
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf

import warnings
warnings.filterwarnings("ignore")



# Create flask app
app = Flask(__name__)

# Load the model
model = load_model('best_model.keras')

def preprocess_image(image_data):
    # Convert the base64 string to an image array
    img = image.img_to_array(image.load_img(image_data, target_size=(224, 224)))
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/predict", methods = ["POST"])
def predict():

    # Get the image data from the request
    # image_data = request.json.get('image')
    image_data = "/media/dibyaruppal/New Volume/IIITB/2nd_sem/SPE/spe_major_project/Project/ai_images_vs_real_image/test/RealArt/33100scr.jpg"
    
    # Preprocess the image
    img = preprocess_image(image_data)
    #print(img)

    # Predict the class of the image
    logits = model.predict(img)
    probabilities = tf.nn.softmax(logits).numpy()
    print(probabilities)
    # predictions contain the probability distribution over classes for each sample
    
    # To get the predicted class labels, you can use argmax
    predicted_labels = tf.argmax(probabilities, axis=1).numpy()

    # Print the predicted labels
    print(predicted_labels)

    if(predicted_labels[0]==1):
        predicted_class = "Real Image"
    elif(predicted_labels[0]==0):
        predicted_class = "AI Generated Image"
    
    return render_template("index.html", prediction_class = predicted_class, predicted_probabilities = probabilities[0])

if __name__ == "__main__":
    app.run(debug=False)