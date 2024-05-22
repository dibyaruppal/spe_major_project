import torch
from torchvision import transforms
from PIL import Image
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import torch.nn as nn
import torch

image_height = 224
image_width = 224
import os

# Define your CNN model in PyTorch
class CustomCNN(nn.Module):
    def __init__(self, num_classes):
        super(CustomCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 56 * 56, 128)  # Adjust the input size based on your image dimensions
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(nn.functional.relu(self.conv1(x)))
        x = self.pool(nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 32 * 56 * 56)  # Adjust the view size based on your image dimensions
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Create an instance of your CNN model and load the model's state dictionary
num_classes = 2
loaded_model = CustomCNN(num_classes)

# Load the model's state dictionary and map it to CPU
model_path = os.getenv('MODEL_PATH', '/mnt/data/best_model.pth')  # Default value
loaded_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

# Set the model to evaluation mode
loaded_model.eval()


def predictClass(image):
    # Load the image and preprocess it
    # image_path = "ai_images_vs_real_image/test/RealArt/end.jpg"s
    if image.mode == 'RGBA':
        image = image.convert('RGB')
        
    preprocess = transforms.Compose([
        transforms.Resize((image_height, image_width)),
        transforms.ToTensor(),
    ])
    img_tensor = preprocess(image).unsqueeze(0)

    # Perform inference on the image
    with torch.no_grad():
        outputs = loaded_model(img_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()  # Move back to CPU for numpy
        predicted_class = np.argmax(probabilities)

    # Print the predicted class and probabilities
    print("Predicted Class:", predicted_class)
    print("Probabilities:", probabilities)
    return {"predictedClass":predicted_class,"prob":probabilities}
    

