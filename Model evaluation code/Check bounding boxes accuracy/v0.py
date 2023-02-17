import os
import cv2
import numpy as np
import torch
import json

# Load the three models
model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Models/D1/best.pt',
                        source='local')

# Set the path to the folder containing the images
img_folder = 'C:/Users/sarpa/Downloads/Leb/images/'

# Set the path to the COCO labels file
labels_file = 'C:/Users/sarpa/Downloads/Leb/annotations/instances_default.json'

# Load the COCO labels
with open(labels_file, 'r') as f:
    labels = json.load(f)

# Create a dictionary to map the image filename to its ID
id_dict = {img_info['file_name']: img_info['id'] for img_info in labels['images']}

# Loop over all images in the folder
for filename in os.listdir(img_folder):
    if filename.lower().endswith('.png'):
        # Load the image
        img_path = os.path.join(img_folder, filename)
        img = cv2.imread(img_path)

        # Print the shape of the loaded image
        #print('Loaded image:', img_path, 'Shape:', img.shape)

        # Make predictions with model1
        results1 = model1(img)
        dat1 = results1.pandas().xyxy[0]
        result1 = dat1.values
        img = np.squeeze(results1.render())

        # Calculate the distance between the predicted bounding box points and the COCO labels bounding box points
        image_id = id_dict[filename]
        for annotation in labels['annotations']:
            if annotation['image_id'] == image_id:
                label_bbox = np.array(annotation['bbox'])  # [xmin, ymin, width, height]
                label_points = np.array(
                    [label_bbox[0], label_bbox[1], label_bbox[0] + label_bbox[2], label_bbox[1] + label_bbox[3]])
                label_center = np.array(
                    [(label_points[0] + label_points[2]) / 2, (label_points[1] + label_points[3]) / 2])
                pred_points = result1[:, :4].astype(int)
                pred_centers = (pred_points[:, :2] + pred_points[:, 2:]) / 2
                distances = np.sqrt(np.sum((pred_centers - label_center) ** 2, axis=1))
                print('Distances between predicted bounding box points and COCO labels bounding box points:', distances)

# Close the window
cv2.destroyAllWindows()