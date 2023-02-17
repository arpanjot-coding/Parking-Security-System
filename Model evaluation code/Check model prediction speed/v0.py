import os
import cv2
import numpy as np
import torch
import json
import time

model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Models/D1/best.pt',
                        source='local')

model2 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Models/D2/best.pt',
                        source='local')

model3 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Models/Tools/best.pt',
                        source='local')

# Set the path to the folder containing the images
img_folder = 'C:/Users/sarpa/Downloads/Leb/images/'

# Loop over all images in the folder
for filename in os.listdir(img_folder):
    if filename.lower().endswith('.png'):
        # Load the image
        img_path = os.path.join(img_folder, filename)
        img = cv2.imread(img_path)

        # Make predictions with model1
        start_time = time.time()
        results1 = model1(img)
        dat1 = results1.pandas().xyxy[0]
        result1 = dat1.values
        img = np.squeeze(results1.render())
        end_time = time.time()
        print(f"Model1 prediction time for {filename}: {end_time - start_time:.3f} seconds")

        # Make predictions with model2
        start_time = time.time()
        results2 = model2(img)
        dat2 = results2.pandas().xyxy[0]
        result2 = dat2.values
        img = np.squeeze(results2.render())
        end_time = time.time()
        print(f"Model2 prediction time for {filename}: {end_time - start_time:.3f} seconds")

        # Make predictions with model3
        start_time = time.time()
        results3 = model3(img)
        dat3 = results3.pandas().xyxy[0]
        result3 = dat3.values
        img = np.squeeze(results3.render())
        end_time = time.time()
        print(f"Model3 prediction time for {filename}: {end_time - start_time:.3f} seconds")
