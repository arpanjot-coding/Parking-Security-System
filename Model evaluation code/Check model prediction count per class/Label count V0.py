import os
import cv2
import numpy as np
import torch
import json
import pandas as pd

# Load the model
model = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/D1/best.pt',
                        source='local')

# Set the path to the folder containing the images
img_folder = 'C:/Users/sarpa/Downloads/Leb/images/'

# Set the path to the COCO labels file
labels_file = 'C:/Users/sarpa/Downloads/Leb/annotations/annotations.json'

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

        # Make predictions with the model
        results = model(img)
        dat = results.pandas().xyxy[0]
        result = dat.values

        # Count the occurrences of each label in the COCO annotations for this image
        image_id = id_dict[filename]
        label_count = {}
        for annotation in labels['annotations']:
            if annotation['image_id'] == image_id:
                label_id = annotation['category_id']
                label_name = id2name[label_id]
                label_count[label_name] = label_count.get(label_name, 0) + 1

        # Append the data for this image to the list
        data.append({
            'image_id': image_id,
            'label_count': label_count
        })

# Convert the list of data to a Pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('output_data.csv', index=False)
