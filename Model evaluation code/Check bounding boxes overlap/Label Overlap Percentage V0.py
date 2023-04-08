import os
import cv2
import numpy as np
import torch
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the three models
model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/D1/best.pt',
                        source='local')

# Set the path to the folder containing the images
img_folder = 'C:/Users/sarpa/Downloads/D1/images/'

# Set the path to the COCO labels file
labels_file = 'C:/Users/sarpa/Downloads/D1/annotations/instances_default.json'

# Load the COCO labels
with open(labels_file, 'r') as f:
    labels = json.load(f)

# Create a dictionary to map the image filename to its ID
id_dict = {img_info['file_name']: img_info['id'] for img_info in labels['images']}

# Create a dictionary to map the category IDs to their names
id2name = {category['id']: category['name'] for category in labels['categories']}

# Create a list to hold the data for each image
data = []

# Loop over all images in the folder
for filename in os.listdir(img_folder):
    if filename.lower().endswith('.png'):
        # Load the image
        img_path = os.path.join(img_folder, filename)
        img = cv2.imread(img_path)

        # Make predictions with model1
        results1 = model1(img)
        dat1 = results1.pandas().xyxy[0]
        result1 = dat1.values
        img = np.squeeze(results1.render())

        # Calculate the overlap percentage between the predicted bounding boxes and the COCO labels bounding boxes
        image_id = id_dict[filename]
        overlaps = []
        for annotation in labels['annotations']:
            if annotation['image_id'] == image_id:
                label_bbox = np.array(annotation['bbox'])  # [xmin, ymin, width, height]
                label_points = np.array(
                    [label_bbox[0], label_bbox[1], label_bbox[0] + label_bbox[2], label_bbox[1] + label_bbox[3]])
                pred_boxes = result1[:, :4].astype(int)
                for pred_box in pred_boxes:
                    pred_points = np.array([pred_box[0], pred_box[1], pred_box[2], pred_box[3]])
                    xA = max(label_points[0], pred_points[0])
                    yA = max(label_points[1], pred_points[1])
                    xB = min(label_points[2], pred_points[2])
                    yB = min(label_points[3], pred_points[3])
                    intersection_area = max(0, xB - xA + 1) * max(0, yB - yA + 1)
                    label_area = (label_points[2] - label_points[0] + 1) * (label_points[3] - label_points[1] + 1)
                    overlap = intersection_area / label_area
                    overlaps.append(overlap)

                # Get the name of the label from the category ID
                label_id = annotation['category_id']
                label_name = id2name[label_id]

                # Get the average overlap for this image
                if overlaps:
                    avg_overlap = np.mean(overlaps)
                else:
                    avg_overlap = np.nan

                # Append the data for this image to the list
                data.append({
                    'image_id': image_id,
                    'label': label_name,
                    'overlaps': overlaps,
                    'avg_overlap': avg_overlap
                })

# Convert the list of data to a Pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('output_data.csv', index=False)
