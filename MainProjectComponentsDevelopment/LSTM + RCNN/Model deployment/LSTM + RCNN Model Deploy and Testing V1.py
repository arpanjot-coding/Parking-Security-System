import cv2
import numpy as np
import tensorflow as tf

# Define the class names list
CLASSES_LIST = ['normal', 'abnormal']

# Load the saved model
model = tf.keras.models.load_model("/content/convlstm_model___Date_Time_2023_01_17__16_31_01___Loss_0.002333042910322547___Accuracy_0.9982788562774658.h5")

def preprocess_frames(video_path, IMAGE_HEIGHT=64, IMAGE_WIDTH=113, SEQUENCE_LENGTH=60):
    frames_list = []

    video_reader = cv2.VideoCapture(video_path)
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    skip_frames_window = max(int(video_frames_count / SEQUENCE_LENGTH), 1)

    for frame_counter in range(SEQUENCE_LENGTH):
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)
        success, frame = video_reader.read()

        if not success:
            break

        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalized_frame = resized_frame / 255
        frames_list.append(normalized_frame)

    video_reader.release()

    return frames_list

def predict_from_video(video_path, model, classes_list):
    preprocessed_frames = preprocess_frames(video_path)
    preprocessed_frames_np = np.expand_dims(preprocessed_frames, axis=0)
    predictions = model.predict(preprocessed_frames_np)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_name = classes_list[predicted_class_index]
    return predicted_class_name

video_path =  "/content/R1.mp4"
predicted_class_name = predict_from_video(video_path, model, CLASSES_LIST)
print(f"Predicted class: {predicted_class_name}")