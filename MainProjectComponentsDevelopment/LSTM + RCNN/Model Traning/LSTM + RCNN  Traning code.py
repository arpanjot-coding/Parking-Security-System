import os
import cv2
import pafy
import random
import numpy as np
import datetime as dt
import tensorflow as tf
import matplotlib.pyplot as plt
from collections import deque
from sklearn.model_selection import train_test_split
from keras.layers import *
from keras.models import Sequential
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.utils import plot_model

# Set the version of TensorFlow to be used
tf.__version__

# Set a seed constant for reproducibility
seed_constant = 27
np.random.seed(seed_constant)
random.seed(seed_constant)
tf.random.set_seed(seed_constant)

# Define image dimensions, sequence length, and dataset directory
IMAGE_HEIGHT, IMAGE_WIDTH = 64, 113
SEQUENCE_LENGTH = 60
DATASET_DIR = "dataset/dataset/"
CLASSES_LIST = ["abnormal", "normal"]


# Function to extract frames from a video file
def frames_extraction(video_path):
    # Declare a list to store video frames.
    frames_list = []

    # Read the Video File using the VideoCapture object.
    video_reader = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video.
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval after which frames will be added to the list.
    skip_frames_window = max(int(video_frames_count / SEQUENCE_LENGTH), 1)

    # Initialize the previous frame variable
    prev_frame = None

    # Iterate through the Video Frames.
    for frame_counter in range(SEQUENCE_LENGTH):

        # Set the current frame position of the video.
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

        # Reading the frame from the video.
        success, frame = video_reader.read()

        # Check if Video frame is not successfully read then break the loop
        if not success:
            break

        # Resize the Frame to fixed height and width.
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))

        # If this is not the first frame, calculate the difference between the current and previous frames
        if prev_frame is not None:
            diff_frame = cv2.absdiff(resized_frame, prev_frame)
            normalized_frame = diff_frame / 255
            frames_list.append(normalized_frame)

        # Update the previous frame
        prev_frame = resized_frame

    # Release the VideoCapture object.
    video_reader.release()

    # Return the frames list.
    return frames_list


# Function to create a dataset with features and labels from the video files
def create_dataset():
    features = []
    labels = []
    video_files_paths = []

    for class_index, class_name in enumerate(CLASSES_LIST):
        print(f'Extracting Data of Class: {class_name}')
        files_list = os.listdir(os.path.join(DATASET_DIR, class_name))
        random.shuffle(files_list)
        i = 0
        l = len(files_list)

        for file_name in files_list:
            if i == 5:
                print(float((i / l) * 100), "%")
            i += 1

            video_file_path = os.path.join(DATASET_DIR, class_name, file_name)
            frames = frames_extraction(video_file_path)
            if len(frames) == SEQUENCE_LENGTH - 1:
                features.append(frames)
                labels.append(class_index)
                video_files_paths.append(video_file_path)

    features = np.asarray(features)
    labels = np.array(labels)
    return features, labels, video_files_paths


# Create the dataset with features and labels
features, labels, video_files_paths = create_dataset()

# One-hot encode the labels
one_hot_encoded_labels = to_categorical(labels)

# Split the dataset into training and testing sets
features_train, features_test, labels_train, labels_test = train_test_split(features, one_hot_encoded_labels,
                                                                            test_size=0.25, shuffle=True,
                                                                            random_state=seed_constant)


# Function to create the 3D CNN model
def create_model():
    model = Sequential()

    # First set of 3D convolutional and pooling layers
    model.add(Conv3D(32, (3, 3, 3), activation='relu', input_shape=(SEQUENCE_LENGTH - 1, IMAGE_HEIGHT, IMAGE_WIDTH, 3)))
    model.add(MaxPool3D(pool_size=(1, 2, 2), strides=(1, 2, 2)))

    # Second set of 3D convolutional and pooling layers
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPool3D(pool_size=(1, 2, 2), strides=(1, 2, 2)))

    # Third set of 3D convolutional and pooling layers
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPool3D(pool_size=(1, 2, 2), strides=(1, 2, 2)))

    # Flatten the output and apply dense layers
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))

    # Dropout layer to reduce overfitting
    model.add(Dropout(0.5))

    # Output layer for classification
    model.add(Dense(len(CLASSES_LIST), activation='softmax'))

    return model

# Create the 3D CNN model
model = create_model()

# Compile the model with appropriate loss function, optimizer, and evaluation metric
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Display the model summary
model.summary()

# Early stopping callback to stop training when the model is not improving
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=10)

# Train the model on the dataset
history = model.fit(features_train, labels_train, batch_size=32, epochs=50, validation_split=0.2,
                    callbacks=[early_stopping_callback])

# Evaluate the model on the test dataset
evaluation = model.evaluate(features_test, labels_test, batch_size=32)

# Plot the training and validation accuracy and loss
plt.figure(figsize=(10, 5))

# Plot the training and validation loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# Plot the training and validation accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# Display the plots
plt.show()




