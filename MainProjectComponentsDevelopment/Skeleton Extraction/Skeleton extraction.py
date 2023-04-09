import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize video file capture
cap = cv2.VideoCapture('C:/Users/sarpa/OneDrive/Desktop/Backup files/Robber-20230408T120506Z-001/Robber/U/20230215_132444.mp4')

# Initialize mediapipe pose detection
with mp_pose.Pose(min_detection_confidence=0.1, min_tracking_confidence=0.1) as pose:
    while cap.isOpened():
        # Read each frame from video
        success, image = cap.read()
        if not success:
            break

        # Convert the image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Convert back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw landmarks
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                landmark.x *= 0.7;landmark.y *= 0.5;landmark.z *= 0.5
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Resize the window to 640x480 pixels
        cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('MediaPipe Pose', 1280, 720)

        # Show detections
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(1) == ord('q'):
            break

# Clean up
cap.release()
cv2.destroyAllWindows()