import os
import torch
from matplotlib import pyplot as plt
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import cv2
import pandas
import time
from ultralytics import YOLO

# Load the three models
model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                             path='C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Models/D1/best.pt',
                             source='local')
model2 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                             path='C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Models/D2/best.pt',
                             source='local')
model3 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                             path='C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Models/Tools/best.pt',
                             source='local')

cap = cv2.VideoCapture('C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Files\Videos/20230215_132444.mp4')


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)
    return resized


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "("+str(self.x)+','+str(self.y)+")"

def do_overlap(O1 , O2):
    l1 = O1['p1']
    r1 = O1['p2']

    l2 = O2['p1']
    r2 = O2['p2']

    if l1.x == r1.x or l1.y == r1.y or r2.x == l2.x or l2.y == r2.y:
        return False

    if l1.x > r2.x or l2.x > r1.x:
        return False

    #if r1.y > l2.y or r2.y > l1.y:
    #    print(r2.y > l1.y)
    #    return False

    return True

def getNumberPlate(frame,data):
    plate = frame[data['p1'].x:data['p2'].x][data['p1'].y:data['p2'].y]
    print(plate)


while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        results1 = model1(frame)
        dat1 = results1.pandas().xyxy[0]
        result1 = dat1.values
        img = np.squeeze(results1.render())

        results2 = model2(img)
        dat2 = results2.pandas().xyxy[0]
        result2 = dat2.values
        img = np.squeeze(results2.render())

        results3 = model3(img)
        dat3 = results3.pandas().xyxy[0]
        result3 = dat3.values
        img = np.squeeze(results3.render())

        RDict = {}
        # if
        for obj in result1:
            if 'Car door open' == obj[-1] and 'CAR' in RDict.keys():
                if RDict['CAR']['C'] > obj[4]:
                    pass
                else:
                    RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4]}

                if obj[4] > 0.70:
                    cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

            elif 'Car door close' == obj[-1] and 'CAR' not in RDict.keys():
                RDict['CAR'] = {'p1': Point(obj[0],obj[1]), 'p2' : Point(obj[2],obj[3]) , 'C' : obj[4]}

            elif 'Car door close' == obj[-1] and 'CAR' in RDict.keys():
                if RDict['CAR']['C'] > obj[4]:
                    pass
                else:
                    RDict['CAR'] = {'p1': Point(obj[0],obj[1]), 'p2' : Point(obj[2],obj[3]) , 'C' : obj[4]}


            elif 'Car door open' == obj[-1] and 'CAR' not in RDict.keys():
                RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4]}

                if obj[4] > 0.70:
                    cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

            elif 'number plate' == obj[-1]:
                if obj[4] > 0.7:
                    RDict['PLATE'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4]}

        for obj in result2:
            if 'Person' == obj[-1]:
                if obj[4] > 0.7:
                    RDict['PERSON'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4]}

            elif 'Security' == obj[-1]:
                if obj[4] > 0.6:
                    RDict['SECURITY'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4]}

        keys = RDict.keys()

        for obj in result3:
            RDict['TOOL'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4]}
            if 'CAR' in keys and 'PERSON' in keys:
                if do_overlap(RDict['TOOL'], RDict['PERSON']) and do_overlap(RDict['TOOL'], RDict['CAR']):
                    cv2.putText(img, "SOMEONE IS BREAKING IN THE CAR", (25, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

        keys = RDict.keys()

        if 'CAR' in keys and 'PERSON' in keys:
            if do_overlap(RDict['CAR'],RDict['PERSON']):
                cv2.putText(img, "MANUAL ROBBERY", (25, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

        if 'PERSON' in keys and 'TOOL' in keys:
            cv2.putText(img, "POTENTIAL ROBBERY", (25, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_4)

        cv2.imshow('YOLO',image_resize(img,width=1000))

        if 'PLATE' in keys:
            getNumberPlate(frame,RDict['PLATE'])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()