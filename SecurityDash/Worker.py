import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import shutil
from moviepy.editor import *


class Worker(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def setVideoMask(self, video, n, msg):
        self.video = video
        self.op = n
        self.msg = msg
        self.framesToStore = []

    def run(self):
        self.ThreadActive = True

        Capture = cv2.VideoCapture(self.op)
        self.fps = Capture.get(cv2.CAP_PROP_FPS)
        print(self.fps)

        frrr = []
        
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                FlippedImage,x = self.video.simulate(FlippedImage, self.msg)

                if x:
                    self.framesToStore.append(FlippedImage)
                elif not x and len(frrr) != 0 and frrr[-1]:
                    self.createVideo(self.framesToStore)
                    self.framesToStore = []

                frrr.append(x)

                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                           QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def createVideo(self,  Array):
        self.msg.addMessage("\tSaving Video .. ", "blue")


        if len(Array) > 5:
            try:
                os.mkdir("DataSet/temp")
            except:
                pass

            clips = []
            for i in range(len(Array)):
                cv2.imwrite("DataSet/temp/img"+str(i)+".jpeg",Array[i])
                clips.append(ImageClip("DataSet/temp/img"+str(i)+".jpeg").set_duration(2))

            video = concatenate_videoclips(clips, method='compose')
            video.write_videofile('DataSet/video 1/test.mp4', fps=self.fps)

            print("check")

        #shutil.rmtree("DataSet/temp")



    def stop(self):
        self.ThreadActive = False
        self.quit()
