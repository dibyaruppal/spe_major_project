import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Check if CUDA is available and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Define your directories and parameters
train_dir = "/mnt/data/ai_images_vs_real_image/train"
test_dir = "/mnt/data/ai_images_vs_real_image/test"
batch_size = 64
image_height = 224
image_width = 224

# Define transforms
transform = transforms.Compose([
    transforms.Resize((image_height, image_width)),
    transforms.ToTensor(),
])

# Load your dataset
train_dataset = datasets.ImageFolder(root=train_dir, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

val_dataset = datasets.ImageFolder(root=test_dir, transform=transform)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)

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

# Create an instance of your CNN model and move it to GPU manually
num_classes = len(train_dataset.classes)
model = CustomCNN(num_classes)
model = model.to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train your model
best_accuracy = 0

train_loss_list = []
train_accuracy_list = []
val_accuracy_list = []
num_epochs = 10

for epoch in range(num_epochs):
    # Training
    model.train()
    train_correct = 0
    train_total = 0
    running_loss = 0.0
    for images, labels in train_loader:
        
        images, labels = images.to(device), labels.to(device)  # Move data to GPU manually
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        _, train_predicted = torch.max(outputs, 1)
        train_total += labels.size(0)
        train_correct += (train_predicted == labels).sum().item()
        
        running_loss += loss.item()
        
    train_accuracy = train_correct / train_total
    avg_train_loss = running_loss / len(train_loader)
    
    # Validation
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)  # Move data to GPU manually
            
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    val_accuracy = correct / total
    
    # Save the model if validation accuracy improves
    if val_accuracy > best_accuracy:
        print("Weights of ",epoch+1," are saved")
        best_accuracy = val_accuracy
        torch.save(model.state_dict(), '/mnt/data/best_model.pth')


    train_loss_list.append(avg_train_loss)
    train_accuracy_list.append(train_accuracy)
    val_accuracy_list.append(val_accuracy)
    print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, Training Accuracy: {train_accuracy:.4f},Validation Accuracy: {val_accuracy:.4f}')

