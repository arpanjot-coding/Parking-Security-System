import sys, time
from random import randrange

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QApplication


class Snake(QWidget):

    score = 0
    x =15
    y =15

    def __init__(self):
        super(Snake, self).__init__()
        self.initUI()

    # Not default method. Just to make the constructor bit tidier.
    # TODO WRITE LINE OF THE NewGame Mehtod and DO NOT TOUCH-> It contains everything related to the window, and it's calling the NewGame method GOTO line ...
    def initUI(self):
        self.highscore = 0
        self.newGame()
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        self.setFixedSize(800, 800)
        self.setWindowTitle('Snake')
        self.show()

    # Default method name
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)

        self.drawSnake(qp)


        qp.end()

    # Default method name
    def keyPressEvent(self, e):
            # print "inflection point: ", self.x, " ", self.y
            if e.key() == QtCore.Qt.Key_Up:
                self.y -=1
            elif e.key() == QtCore.Qt.Key_Down:
                self.y += 1
            elif e.key() == QtCore.Qt.Key_Left:
                self.x -= 1
            elif e.key() == QtCore.Qt.Key_Right:
                self.x += 1

            print(f"X={self.x} Y={self.y}")

    # Not default method.
    def newGame(self):
        self.timer = QtCore.QBasicTimer()
        self.speed = 100



        self.start()

    # Not default method.
    def pause(self):
        self.isPaused = True
        self.timer.stop()
        self.update()

    # Not default method.
    def start(self):
        self.isPaused = False
        self.timer.start(self.speed, self)
        self.update()

    # Not default method.
    def update(self, ):
        # The code bellow is just to show how it is adding numbers
        #     self.score +=1
        #     print(self.score)

        # The
            self.repaint()




    # Not default method.
    def drawSnake(self, qp):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 80, 0, 255))
        qp.drawRect(self.x, self.y, 12, 12)
        qp.drawRect(200, 200, 210, 210)

    # Default method name
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            # The code bellow is used to
            self.update()
            self.repaint()
        else:
            QtGui.QFrame.timerEvent(self, event)


def main():
    app = QApplication(sys.argv)
    ex = Snake()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()