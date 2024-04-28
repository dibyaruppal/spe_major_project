import numpy as np 
import pandas as pd 
from sklearn.metrics import classification_report, f1_score

import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense, BatchNormalization, Conv2D, Dropout, MaxPooling2D, Flatten, Rescaling
from keras.optimizers import Adam

from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

import matplotlib
import matplotlib.pyplot as plt


import os
from IPython.display import Image
import warnings
warnings.filterwarnings("ignore")



# Function for plotting the error rate and metrics rate
def plot_metrics(history, metric):
    plt.plot(history.history[metric], label = metric)
    plt.plot(history.history['val_' + metric], label='val_' + metric)
    plt.xlabel('Epochs')
    plt.ylabel(metric)
    plt.legend()
    plt.show()



train_dir = "D:/IIITB/2nd_sem/SPE/spe_major_project/Project/ai_images_vs_real_image/train"
test_dir  = "D:/IIITB/2nd_sem/SPE/spe_major_project/Project/ai_images_vs_real_image/test"
batch_size = 64
image_height = 224
image_width = 224
num_channels = 3



train_ds = tf.keras.utils.image_dataset_from_directory(
                train_dir,
                seed=42,
                image_size=(image_height, image_width),
                batch_size=batch_size
            )



valid_ds = tf.keras.utils.image_dataset_from_directory(
                test_dir,
                seed=42,
                image_size=(image_height, image_width),
                batch_size=batch_size
            )



train_class_names = train_ds.class_names
print(train_class_names)
num_classes_train = len(train_class_names)
print(num_classes_train)



test_class_names = valid_ds.class_names
print(test_class_names)
num_classes_test = len(test_class_names)
print(num_classes_test)



plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(train_class_names[labels[i]])
        plt.axis("off")



normalization_layer =  Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
valid_ds = valid_ds.map(lambda x, y: (normalization_layer(x), y))



AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
valid_ds = valid_ds.cache().prefetch(buffer_size=AUTOTUNE)



def plot_training_history(history, accuracy = 'accuracy'):
    train_acc = history.history[accuracy]
    train_loss = history.history['loss']

    val_acc = history.history['val_' + accuracy]
    val_loss = history.history['val_loss']

    index_loss = np.argmin(val_loss)
    val_lowest = val_loss[index_loss]

    index_acc = np.argmax(val_acc)
    val_highest = val_acc[index_acc]

    Epochs = [i+1 for i in range(len(train_acc))]

    loss_label = f'Best epochs = {str(index_loss +1)}'
    acc_label = f'Best epochs = {str(index_acc + 1)}'

    # Training history
    plt.figure(figsize= (20,8))
    plt.style.use('fivethirtyeight')

    plt.subplot(1,2,1)
    plt.plot(Epochs , train_loss , 'r' , label = 'Training Loss')
    plt.plot(Epochs , val_loss , 'g' , label = 'Validation Loss')
    plt.scatter(index_loss + 1 , val_lowest , s = 150 , c = 'blue',label = loss_label)
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(Epochs , train_acc , 'r' , label = 'Training Accuracy')
    plt.plot(Epochs , val_acc , 'g' , label = 'Validation Accuracy')
    plt.scatter(index_acc + 1 , val_highest , s = 150 , c = 'blue',label = acc_label)
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.tight_layout
    plt.show()



num_classes = len(train_class_names)

# Define the CNN model
model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(128, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(256, 3, padding='same', activation='relu'),
    BatchNormalization(),
    MaxPooling2D(),
    
    Flatten(),
    
    Dense(128, activation='relu'),
    Dense(num_classes)
])


optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001)
loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer=optimizer,loss=loss,metrics=['sparse_categorical_accuracy'])



# Define early stopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_sparse_categorical_accuracy', patience=10, restore_best_weights=True)

# Define model checkpoint callback to save the best model
model_checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model.keras', 
                                                      monitor='val_sparse_categorical_accuracy', 
                                                      save_best_only=True, 
                                                      mode='max', 
                                                      verbose=1)




# Train the model with early stopping
history = model.fit(train_ds,
                    epochs=50, 
                    validation_data=valid_ds, 
                    callbacks=[ model_checkpoint])




plot_training_history(history, 'sparse_categorical_accuracy')


# Load the saved model
model = load_model("D:/IIITB/2nd_sem/SPE/spe_major_project/Project/working/best_model.keras")


# Assuming X_test contains the test data
# Make predictions on the test data
logits = model.predict(valid_ds)
probabilities = tf.nn.softmax(logits).numpy()
# predictions contain the probability distribution over classes for each sample
# To get the predicted class labels, you can use argmax
predicted_labels = tf.argmax(probabilities, axis=1)

# Print the predicted labels
print(predicted_labels)



true_indices = []
for i, record in enumerate(valid_ds.unbatch()):
    image, label = record
    true_indices.append(label.numpy())
    
len(true_indices)



# Calculate accuracy
accuracy = accuracy_score(true_indices, predicted_labels)
print("\nAccuracy:", accuracy)

# Calculate F1 score
score_f1 = f1_score(true_indices, predicted_labels)
print("\nF1 Score:", score_f1)

# Print classification report
print("\nClassification Report:")
print(classification_report(true_indices, predicted_labels))