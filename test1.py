import sys
from PyQt5.QtWidgets import (QMainWindow,QApplication,QDialog,
QHBoxLayout, QVBoxLayout, QGroupBox, QWidget, QPushButton)
from PyQt5 import QtGui
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


class WindowWidgets(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        self.createLayout1()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

    def createLayout1(self):
        hboxlayout = QHBoxLayout()
        # hboxlayout.setSizeConstraint(QLayout.SetFixedSize)
        self.groupBox = QGroupBox("GroupBox")

        win = pg.GraphicsWindow()
        win.setWindowTitle('pyqtgraph example: Scrolling Plots')

        p1 = win.addPlot()
        p2 = win.addPlot()
        data1 = np.random.normal(size=300)
        curve1 = p1.plot(data1)
        curve2 = p2.plot(data1)
        ptr1 = 0
        def update1():
            global data1, curve1, ptr1
            data1[:-1] = data1[1:]  # shift data in the array one sample left
                                    # (see also: np.roll)
            data1[-1] = np.random.normal()
            curve1.setData(data1)

            ptr1 += 1
            curve2.setData(data1)
            curve2.setPos(ptr1, 0)

        def update():
            update1()
        def StartTime():
            self.timer = pg.QtCore.QTimer()
            self.timer.timeout.connect(update)
            self.timer.start(50)
            print("started")

        okButton = QPushButton("OK")
        okButton.clicked.connect(StartTime)
        hboxlayout.addWidget(okButton)

        self.groupBox.setLayout(hboxlayout)




class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("App Title")
        self.setGeometry(500, 200, 800, 800)

        hboxlayout = QHBoxLayout()
        tests = WindowWidgets()
        hboxlayout.addWidget(tests)
        self.setLayout(hboxlayout)

        self.show()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
