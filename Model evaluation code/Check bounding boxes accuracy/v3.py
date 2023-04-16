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

        # Calculate the distance between the predicted bounding box points and the COCO labels bounding box points
        image_id = id_dict[filename]
        distances = []
        for annotation in labels['annotations']:
            if annotation['image_id'] == image_id:
                label_bbox = np.array(annotation['bbox'])  # [xmin, ymin, width, height]
                label_points = np.array(
                    [label_bbox[0], label_bbox[1], label_bbox[0] + label_bbox[2], label_bbox[1] + label_bbox[3]])
                label_center = np.array(
                    [(label_points[0] + label_points[2]) / 2, (label_points[1] + label_points[3]) / 2])
                pred_points = result1[:, :4].astype(int)
                pred_centers = (pred_points[:, :2] + pred_points[:, 2:]) / 2
                dist = np.sqrt(np.sum((pred_centers - label_center) ** 2, axis=1))
                distances.extend(dist)

                # Get the name of the label from the category ID
                label_id = annotation['category_id']
                label_name = id2name[label_id]

                # Get the average distance for this image
                if distances:
                    avg_distance = np.mean(distances)
                else:
                    avg_distance = np.nan

                # Append the data for this image to the list
                data.append({
                    'image_id': image_id,
                    'label': label_name,
                    'distances': dist,
                    'avg_distance': avg_distance
                })

        # # Set the flag variable to True
        # continue_loop = True
        #
        # # Loop over all images in the folder
        # for filename in os.listdir(img_folder):
        #
        #     if filename.lower().endswith('.png'):
        #         # Load the image
        #         img_path = os.path.join(img_folder, filename)
        #         img = cv2.imread(img_path)
        #
        #         # Make predictions with model1
        #         results1 = model1(img)
        #         dat1 = results1.pandas().xyxy[0]
        #         result1 = dat1.values
        #         img = np.squeeze(results1.render())
        #
        #         # Visualize the bounding boxes
        #         for bbox in result1[:, :4].astype(int):
        #             cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        #         for annotation in labels['annotations']:
        #             if annotation['image_id'] == id_dict[filename]:
        #                 label_bbox = np.array(annotation['bbox'])  # [xmin, ymin, width, height]
        #                 label_points = np.array(
        #                     [label_bbox[0], label_bbox[1], label_bbox[0] + label_bbox[2],
        #                      label_bbox[1] + label_bbox[3]])
        #                 label_points = tuple(label_points.astype(int))
        #                 cv2.rectangle(img, label_points[:2], label_points[2:], (0, 0, 255), 2)
        #                 cv2.putText(img, 'COCO', (label_points[0], label_points[1] - 10),
        #                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #
        #         # Display the image with the bounding boxes
        #         cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        #         cv2.resizeWindow('image', 1200, 800)
        #         cv2.imshow('image', img)
        #
        #         # Wait for a key press and check if the 'e' key is pressed
        #         key = cv2.waitKey(1000)
        #         if key == ord('e'):
        #             # Destroy the cv2 window
        #             cv2.destroyAllWindows()



# Convert the list of data to a Pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('output_data.csv', index=False)

