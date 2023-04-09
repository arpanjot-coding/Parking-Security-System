import cv2
import numpy as np
import tensorflow as tf

# Define the class names list
CLASSES_LIST = ['abnormal', 'normal']

# Load the saved model
model = tf.keras.models.load_model("/content/convlstm_model___Date_Time_2023_01_17__16_31_01___Loss_0.002333042910322547___Accuracy_0.9982788562774658.h5")

def preprocess_frames(frames, IMAGE_HEIGHT=64, IMAGE_WIDTH=113, SEQUENCE_LENGTH=60):
    frames_list = []

    skip_frames_window = max(int(len(frames) / SEQUENCE_LENGTH), 1)
    total_frames_to_process = min(len(frames), SEQUENCE_LENGTH * skip_frames_window)

    for frame_counter in range(0, total_frames_to_process, skip_frames_window):
        frame = frames[frame_counter]

        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalized_frame = resized_frame / 255
        frames_list.append(normalized_frame)

    return frames_list

def predict_from_video(video_path, model, classes_list):
    video_reader = cv2.VideoCapture(video_path)
    fps = int(video_reader.get(cv2.CAP_PROP_FPS))
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    one_second_frames = fps
    total_clips = int(video_frames_count / one_second_frames)

    for clip_number in range(total_clips):
        clip_frames = []

        for _ in range(one_second_frames):
            success, frame = video_reader.read()

            if not success:
                break

            clip_frames.append(frame)

        preprocessed_frames = preprocess_frames(clip_frames)
        preprocessed_frames_np = np.expand_dims(preprocessed_frames, axis=0)
        predictions = model.predict(preprocessed_frames_np)
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = classes_list[predicted_class_index]

        print(f"Predicted class for clip {clip_number + 1}: {predicted_class_name}")

    video_reader.release()

video_path = "/content/0223 - Trim.mp4"
predict_from_video(video_path, model, CLASSES_LIST)