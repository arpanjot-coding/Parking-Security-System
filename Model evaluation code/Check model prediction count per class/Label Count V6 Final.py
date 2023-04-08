import os
import cv2
import numpy as np
import torch
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the three models
model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='Models/D1/best.pt',
                        source='local')

# Set the path to the folder containing the images
img_folder = 'C:/Users/sarpa/Downloads/D1/images/'

# Set the path to the COCO labels file
labels_file = 'C:/Users/sarpa/Downloads/D1/annotations/instances_default.json'

# Load the COCO labels
with open(labels_file, 'r') as f:
    labels = json.load(f)

# Create a dictionary to map the category IDs to their names
id2name = {category['id']: category['name'] for category in labels['categories']}

# Create a dictionary to map the image filename to its ID
id_dict = {img_info['file_name']: img_info['id'] for img_info in labels['images']}

# Create a list to hold the data for each image
data = []

# Loop over all images in the folder
for filename in os.listdir(img_folder):
    if filename.lower().endswith('.png'):
        # Load the image
        img_path = os.path.join(img_folder, filename)
        img = cv2.imread(img_path)

        # Initialize label counters for this image
        model1_label_counts = {id2name[category_id]: 0 for category_id in id2name.keys()}
        coco_label_counts = {id2name[category_id]: 0 for category_id in id2name.keys()}

        # Make predictions with model1
        results1 = model1(img)
        dat1 = results1.pandas().xyxy[0]
        result1 = dat1.values
        img = np.squeeze(results1.render())

        # Update model1 label counts
        for bbox in result1:
            category_id = int(bbox[5])
            if category_id in id2name:
                label = id2name[category_id]
                if label == 'Car door close':
                    model1_label_counts['Car door open'] += 1
                elif label == 'Car door open':
                    model1_label_counts['Car door close'] += 1
                else:
                    model1_label_counts[label] += 1

        # Update COCO label counts and store predictions
        coco_predictions = {}
        img_id = id_dict[filename]
        for annotation in labels['annotations']:
            if annotation['image_id'] == img_id:
                category_id = annotation['category_id']
                if category_id in id2name:
                    label = id2name[category_id]
                    coco_label_counts[label] += 1

        # Store data for this image
        data.append({
            'filename': filename,
            'model1': model1_label_counts.copy(),
            'coco': coco_label_counts.copy()
        })

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('output_data.csv', index=False)
