from PyQt5.QtWidgets import *
from Messages import ErrorWidget
from PyQt5.QtCore import *
from CameraFeed import CameraFeed
from Simulation import MainSimulation


class MyTableWidget(QWidget):

    def __init__(self, m1, m2, m3, userData):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.userData = userData
        # Initialize tab screen
        self.tabs = QTabWidget()
        # self.addTAB()

        tabBtn = QPushButton('ADD NEW TAB')
        tabBtn.clicked.connect(self.addTAB)

        self.tabs.resize(1100, 700)
        self.ew = ErrorWidget()
        # Add tabs to widget
        self.layout.addWidget(tabBtn)
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

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
