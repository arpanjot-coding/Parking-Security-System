import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Define the class names list
CLASSES_LIST = ['normal', 'abnormal']

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

    normal_frames = []
    abnormal_frames = []

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

        if predicted_class_name == 'normal' and len(normal_frames) < 10:
            normal_frames.append(clip_frames[59])
        elif predicted_class_name == 'abnormal' and len(abnormal_frames) < 10:
            abnormal_frames.append(clip_frames[59])

        if len(normal_frames) >= 10 and len(abnormal_frames) >= 10:
            break

    video_reader.release()
    return normal_frames, abnormal_frames

def plot_frames(normal_frames, abnormal_frames):
    fig, axes = plt.subplots(nrows=2, ncols=10, figsize=(25, 5))
    fig.suptitle('60th Frame of Predicted Clips (Top: Normal, Bottom: Abnormal)', fontsize=20)

    for i, frame in enumerate(normal_frames):
        axes[0, i].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        axes[0, i].axis('off')
    for i, frame in enumerate(abnormal_frames):
        axes[1, i].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        axes[1, i].axis('off')

    plt.show()

video_path = "/content/0223 - Trim.mp4"
normal_frames, abnormal_frames = predict_from_video(video_path, model, CLASSES_LIST)
plot_frames(normal_frames, abnormal_frames)