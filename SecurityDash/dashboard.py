from PyQt5.QtWidgets import *
from Messages import ErrorWidget
from PyQt5.QtCore import *
from CameraFeed import CameraFeed
from Simulation import MainSimulation
from HistoryWindow import AnotherWindow
from PyQt5 import QtWidgets
import sys

class MyTableWidget(QWidget):

    def __init__(self,widget, m1, m2, m3, userData):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.Blayout = QHBoxLayout(self)
        self.userData = userData
        self.widget = widget
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.setStyleSheet("background-color: grey;")
        # self.addTAB()

        tabBtn = QPushButton('ADD NEW TAB')
        tabBtn.clicked.connect(self.addTAB)

        Notif = QPushButton("History")
        Notif.clicked.connect(self.showHistoryWindow)

        self.tabs.resize(1100, 700)
        self.ew = ErrorWidget()

        # Add tabs to widget
        self.Blayout.addWidget(tabBtn)
        self.Blayout.addWidget(Notif)

        self.layout.addLayout(self.Blayout)
        self.layout.addWidget(self.ew)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.model1 = m1
        self.model2 = m2
        self.model3 = m3

    def addTAB(self):
        name, done1 = QInputDialog.getText(self, 'Input Dialog', 'Enter video Id/Name :')
        if done1:
            self.ew.addMessage("Tab " + name + " Added", "lightgreen")
            tab1 = QWidget()
            self.tabs.addTab(tab1, "VIDEO " + str(name))
            tab1.layout = QHBoxLayout(self)
            mask = MainSimulation(self.model1, self.model2, self.model3, self.ew, name, self.userData)

            tab1.layout.addWidget(CameraFeed(mask, name, self.ew))
            tab1.layout.addWidget(mask)

            tab1.setLayout(tab1.layout)
            # Add tabs to widget
            self.layout.addWidget(self.tabs)
            self.setLayout(self.layout)

    def showHistoryWindow(self):
        AnotherWindow("DataSet/")

    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
