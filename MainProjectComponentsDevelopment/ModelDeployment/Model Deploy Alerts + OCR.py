import torch
import numpy as np
import cv2.version
import time
import os


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

cap = cv2.VideoCapture('C:/Users/sarpa/PycharmProjects/FYP-Arpanjot_Singh/TestingResources/Files/Videos/20230215_132444.mp4')

dateEnd = "4/2/2023"
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

    return True

def getNumberPlate(frame,data):
    cv2.imwrite("test/n.jpg",frame)
    reader = easyocr.Reader(['en'])
    output = reader.readtext("test/n.jpg")

    num = ""
    for i in output:
        num+=i[1]
    return num

def verifyDate(date):
    t = time.localtime()
    return (str(t[2])+"/"+str(t[1])+"/"+str(t[0])) == date

while cap.isOpened():
    # reading frame and success of the frame
    ret, frame = cap.read()
    # if successful then checking conditions
    if ret:
        # Getting predictions from model1 about frame
        results1 = model1(frame)
        dat1 = results1.pandas().xyxy[0]
        result1 = dat1.values
        img = np.squeeze(results1.render())

        # Getting predictions from model2 about frame
        results2 = model2(img)
        dat2 = results2.pandas().xyxy[0]
        result2 = dat2.values
        img = np.squeeze(results2.render())

        # Getting predictions from model1 about frame
        results3 = model3(img)
        dat3 = results3.pandas().xyxy[0]
        result3 = dat3.values
        img = np.squeeze(results3.render())

        # img is the final image with bounding boxes from all the images.

        RDict = {}  # used to collect the information about the frame in dictionary.
        i = 0
        CarDoorOpen = False

        # count the number of cars available or person etc...
        carCount = 1
        personCount = 1
        numberPlateCount = 1
        toolCount = 1
        securityCount = 1

        # now first of all lets get the objects of model 1 results
        for obj in result1:
            # checking 'car door open' object is available in results
            if 'Car door open' == obj[
                -1] and 'CAR' in RDict.keys():  # and if the 1 'CAR' was already there in the dictionary
                if RDict['CAR']['C'] > obj[4]:
                    RDict['CAR']['count'] += 1
                    # if the model is confusing the 'car door open and car door close then take car with high confidence
                else:
                    # collect the car
                    RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                         'count': carCount}
                    carCount += 1

                # if car door is open and the confidence is above 70% then say the car door is open
                if obj[4] > 0.70:
                    CarDoorOpen = True
                    # writing on frame that the car door is open
                    cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

            elif 'Car door close' == obj[-1] and 'CAR' not in RDict.keys():
                # checking 'car door close' object is available in results and adding it to the dictionary
                RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                     'count': carCount}
                carCount += 1

            elif 'Car door close' == obj[
                -1] and 'CAR' in RDict.keys():  # and if the 1 'CAR' was already there in the dictionary
                # checking 'car door close' object is available in results
                if RDict['CAR']['C'] > obj[4]:
                    RDict['CAR']['count'] += 1
                else:
                    # collect the car
                    RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                         'count': carCount}
                    carCount += 1

            elif 'Car door open' == obj[-1] and 'CAR' not in RDict.keys():
                # checking 'car door open' object is available in results and adding it to the dictionary
                RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                     'count': carCount}
                carCount += 1
                # if car door is open and the confidence is above 70% then say the car door is open
                if obj[4] > 0.70:
                    # writing on frame that the car door is open
                    CarDoorOpen = True
                    cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

            elif 'number plate' == obj[-1]:
                # checking 'number plate' object is available in results and adding it to the dictionary
                RDict['PLATE'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                       'count': numberPlateCount}
                numberPlateCount += 1

        # now lets get the objects of model 2 results
        for obj in result2:
            # checking 'Person' object is available in results and adding it to the dictionary
            if 'Person' == obj[-1]:
                # if Person is in frame and the confidence is above 70% then person is confirm
                if obj[4] > 0.5:
                    RDict['PERSON'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                            'count': personCount}
                    personCount += 1

            # checking 'Security' object is available in results and adding it to the dictionary
            elif 'Security' == obj[-1]:
                # if Security is in frame and the confidence is above 70% then person is confirm
                if obj[4] > 0.6:
                    RDict['SECURITY'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                              'count': securityCount}
                    securityCount += 1

        keys = RDict.keys()

        # getting the results of Tools model
        for obj in result3:
            # Storing the TOOL information in the Dictionary
            RDict['TOOL'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                  'count': toolCount}
            toolCount += 1

            # Checking if the CAR is in frame and the PERSON is also there
            if 'CAR' in keys and 'PERSON' in keys:
                # checking if the person is intersecting with the tools or not
                if do_overlap(RDict['TOOL'], RDict['PERSON']) and do_overlap(RDict['TOOL'],RDict['CAR']):
                    # if intersecting then saying 'someone is trying to breakin"
                    cv2.putText(img, "SOMEONE IS BREAKING IN THE CAR", (25, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255), 3, cv2.LINE_4)

        keys = RDict.keys()

        # Checking if the car is in frame + person is also present + if car door is open or not + is today the checkin date or not
        if 'CAR' in keys and 'PERSON' in keys and CarDoorOpen and not verifyDate(dateEnd):
            # if car and person is overlaping then saying its 'manual robbery'
            if do_overlap(RDict['CAR'], RDict['PERSON']):
                cv2.putText(img, "MANUAL ROBBERY", (25, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

        # if tool and person is intersecting then saying 'potential robbery'
        if 'PERSON' in keys and 'TOOL' in keys and do_overlap(RDict['TOOL'], RDict['PERSON']):
            cv2.putText(img, "POTENTIAL ROBBERY", (25, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_4)

        # displaying the frame
        cv2.imshow('YOLO', image_resize(img, width=1000))

        if 'CAR' in keys and 'PERSON' in keys:
            pass

cap.release()
cv2.destroyAllWindows()