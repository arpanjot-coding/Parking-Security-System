import torch
import cv2
from threading import Thread
import random


class ThreadWithReturnValue(Thread):

    def _init_(self, group=None, target=None, name=None,
               args=(), kwargs={}, Verbose=None):
        Thread._init_(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


# Load the three models
model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='Models/D1/best.pt',
                        source='local')

model2 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='Models/D2/best.pt',
                        source='local')

model3 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                        path='Models/Tools/best.pt',
                        source='local')

cap = cv2.VideoCapture('C:/Users/sarpa/OneDrive/Desktop/DataSet Label/Videos/20230215_132444.mp4')


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
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

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized


def getResult(model,frame):
    result = model(frame)
    dat = result.pandas().xyxy[0]
    result = dat.values

    boxes = {}
    for obj in result:
        if obj[-1] not in list(boxes.keys()):
            boxes[obj[-1]] = [(int(obj[0]), int(obj[1])), (int(obj[2]), int(obj[3]))]
        else:
            boxes[obj[-1]+str(random.randint(1,10))] = [(int(obj[0]), int(obj[1])), (int(obj[2]), int(obj[3]))]
    return boxes


while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        t1 = ThreadWithReturnValue(target=getResult, args=(model1,frame))
        t2 = ThreadWithReturnValue(target=getResult, args=(model2,frame))
        t3 = ThreadWithReturnValue(target=getResult, args=(model3,frame))


        t1.start()
        t2.start()
        t3.start()

        res1 = t1.join()
        res2 = t2.join()
        res3 = t3.join()


        for i in res1.values():
            cv2.rectangle(frame, i[0], i[1], (255,0,0), 2)

        for i in res2.values():
            cv2.rectangle(frame, i[0], i[1], (255, 0, 0), 2)

        for i in res3.values():
            cv2.rectangle(frame, i[0], i[1], (255, 0, 0), 2)

        cv2.imshow('YOLO', image_resize(frame, width=1000))

        cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
