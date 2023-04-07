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
img_folder = 'C:/Users/sarpa/Downloads/Leb/images/'

# Set the path to the COCO labels file
labels_file = 'C:/Users/sarpa/Downloads/Leb/annotations/annotations.json'

# Load the COCO labels
with open(labels_file, 'r') as f:
    labels = json.load(f)

# Create a dictionary to map the category IDs to their names
id2name = {category['id']: category['name'] for category in labels['categories']}

# Create a dictionary to map the image filename to its ID
id_dict = {img_info['file_name']: img_info['id'] for img_info in labels['images']}


# Create a list to hold the data for each image
data = []

# Initialize label counters
model1_label_counts = {id2name[category_id]: 0 for category_id in id2name.keys()}
coco_label_counts = {id2name[category_id]: 0 for category_id in id2name.keys()}

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

        # Update model1 label counts
        for bbox in result1:
            category_id = int(bbox[5])
            if category_id in id2name:
                model1_label_counts[id2name[category_id]] += 1

        # Update COCO label counts
        img_id = id_dict[filename]
        for annotation in labels['annotations']:
            if annotation['image_id'] == img_id:
                category_id = annotation['category_id']
                if category_id in id2name:
                    coco_label_counts[id2name[category_id]] += 1

# Print label counts
print("Model1 label counts:")
for label, count in model1_label_counts.items():
    print(f"{label}: {count}")

print("\nCOCO label counts:")
for label, count in coco_label_counts.items():
    print(f"{label}: {count}")