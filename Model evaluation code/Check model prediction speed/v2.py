import os
import cv2
import numpy as np
import torch
import json
import time
import psutil
import pandas as pd


model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/D1/best.pt',
                        source='local')

model2 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/D2/best.pt',
                        source='local')

model3 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/Tools/best.pt',
                        source='local')

# Set the path to the folder containing the images
img_folder = 'C:/Users/sarpa/Downloads/Leb/images/'

# Create an empty list to store the output data
output_data = []

# Loop over all images in the folder
for filename in os.listdir(img_folder):
    if filename.lower().endswith('.png'):
        # Load the image
        img_path = os.path.join(img_folder, filename)
        img = cv2.imread(img_path)

        # Get the current CPU usage
        cpu_percent_start = psutil.cpu_percent()

        # Make predictions with model1
        start_time = time.time()
        results1 = model1(img)
        dat1 = results1.pandas().xyxy[0]
        result1 = dat1.values
        img = np.squeeze(results1.render())
        end_time = time.time()
        prediction_time1 = end_time - start_time
        cpu_percent_model1 = psutil.cpu_percent() - cpu_percent_start

        # Make predictions with model2
        start_time = time.time()
        results2 = model2(img)
        dat2 = results2.pandas().xyxy[0]
        result2 = dat2.values
        img = np.squeeze(results2.render())
        end_time = time.time()
        prediction_time2 = end_time - start_time
        cpu_percent_model2 = psutil.cpu_percent() - cpu_percent_model1

        # Make predictions with model3
        start_time = time.time()
        results3 = model3(img)
        dat3 = results3.pandas().xyxy[0]
        result3 = dat3.values
        img = np.squeeze(results3.render())
        end_time = time.time()
        prediction_time3 = end_time - start_time
        cpu_percent_model3 = psutil.cpu_percent() - cpu_percent_model2

        # Append the output data to the list
        output_data.append([filename, result1, result2, result3, prediction_time1, prediction_time2, prediction_time3,
                            cpu_percent_model1, cpu_percent_model2, cpu_percent_model3])

# Create a DataFrame to store the output data
columns = ['Filename', 'Model1 Output', 'Model2 Output', 'Model3 Output', 'Model1 Prediction Time', 'Model2 Prediction Time', 'Model3 Prediction Time', 'Model1 CPU Usage', 'Model2 CPU Usage', 'Model3 CPU Usage']
df = pd.DataFrame(output_data, columns=columns)

# Save the DataFrame to a CSV file
df.to_csv('output_data.csv', index=False)

