import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Define the class names list
CLASSES_LIST = ['abnormal','normal']

# Load the saved model
model = tf.keras.models.load_model( "C:/Users/sarpa/OneDrive/Desktop/convlstm_model___Date_Time_2023_01_17__16_31_01___Loss_0.002333042910322547___Accuracy_0.9982788562774658.h5")


def preprocess_frames(frames, IMAGE_HEIGHT=64, IMAGE_WIDTH=113, SEQUENCE_LENGTH=60):
    frames_list = []

    skip_frames_window = max(int(len(frames) / SEQUENCE_LENGTH), 1)

    for frame_counter in range(SEQUENCE_LENGTH):
        frame = frames[frame_counter * skip_frames_window]

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

    true_labels = []
    predicted_labels = []

    for clip_number in range(total_clips):
        clip_frames = []

        for _ in range(one_second_frames):
            success, frame = video_reader.read()

            if not success:
                break

            clip_frames.append(frame)

        # Show the last frame of the clip, resized to 1080x720
        resized_frame = cv2.resize(clip_frames[-1], (1080, 720))
        cv2.imshow(f"Clip {clip_number + 1} - Last Frame", resized_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        preprocessed_frames = preprocess_frames(clip_frames)
        preprocessed_frames_np = np.expand_dims(preprocessed_frames, axis=0)
        predictions = model.predict(preprocessed_frames_np)
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = classes_list[predicted_class_index]

        true_label = input(f"Enter the true label for clip {clip_number + 1} (normal or abnormal): ").lower().strip()
        while true_label not in CLASSES_LIST:
            true_label = input("Invalid input. Please enter either 'normal' or 'abnormal': ").lower().strip()

        true_labels.append(true_label)
        predicted_labels.append(predicted_class_name)

    video_reader.release()
    return true_labels, predicted_labels


def plot_confusion_matrix(y_true, y_pred, classes_list):
    cm = confusion_matrix(y_true, y_pred, labels=classes_list)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)

    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes_list, yticklabels=classes_list,
           title="Confusion Matrix",
           ylabel='True label',
           xlabel='Predicted label')

    plt.show()


video_path = "C:/Users/sarpa/OneDrive/Desktop/LRN TESTTING/0223 - Trim.mp4"
true_labels, predicted_labels = predict_from_video(video_path, model, CLASSES_LIST)
plot_confusion_matrix(true_labels, predicted_labels, CLASSES_LIST)
