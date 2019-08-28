# https://www.swharden.com/wp/page/5/
# https://pythonprogramminglanguage.com/pyqt-textarea/

import sys, time, random
from PyQt5.QtWidgets import (QMainWindow,QApplication,QDialog,
QHBoxLayout, QVBoxLayout, QGroupBox, QWidget, QPushButton,
QSlider, QGridLayout)
from PyQt5 import  QtWidgets, QtGui, Qt
from PyQt5.QtCore import Qt as QTC
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from XAxisTime import TimeAxisItem, timestamp


class WindowPlot(QMainWindow):
    def __init__(self, parent=None):
        pg.setConfigOption('background', 'w') #before loading widget
        super(WindowPlot, self).__init__(parent)

        self.RNDbtn = False
        self.data = [] #np.random.normal(size=100)
        self.Xtime = []
        self.refreshInterval = 1000 # default refresh plot every 1s
        self.timer = pg.QtCore.QTimer()
        self.TimerFirstRun = True

        self.wid = QtGui.QWidget(self)
        self.setCentralWidget(self.wid)

        vbox = QVBoxLayout()
        self.createLayout1()
        vbox.addWidget(self.groupBox)
        self.wid.setLayout(vbox)

        self.show()

    def createLayout1(self):
        vboxlayout = QVBoxLayout()
        self.groupBox = QGroupBox("GroupBox")
        self.create_plot()
        vboxlayout.addLayout(self.layout)

        self.grid = QGridLayout()

        self.GetDataBtn = QPushButton("Connect")
        self.GetDataBtn.clicked.connect(self.ticker)
        self.GetDataBtn.setMinimumHeight(50)
        self.GetDataBtn.setMinimumWidth(180)

        self.slider = QSlider(QTC.Horizontal)
        self.slider.setFocusPolicy(QTC.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setMaximum(10)
        self.slider.setMinimum(0)
        # self.slider.valueChanged.connect(self.SliderVal)
        self.slider.setValue(7)

        self.cb = QtWidgets.QComboBox()
        # self.cb.addItem("10")
        self.cb.addItems(["5000", "2000", "1000"])
        self.cb.setCurrentIndex(2)
        self.cb.currentIndexChanged.connect(self.ComboInterval)

        self.grid.addWidget(self.slider, 0, 0)
        self.grid.addWidget(self.cb, 0, 1)
        self.grid.addWidget(self.GetDataBtn, 1, 1)

        vboxlayout.addLayout(self.grid)
        self.groupBox.setLayout(vboxlayout)

    # def SliderVal(self):
    #     print(self.slider.value())
    def ComboInterval(self):
        self.refreshInterval = int(self.cb.currentText())
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(self.refreshInterval)

    def create_plot(self):

        self.stream_scroll = pg.PlotWidget(
            title='Stream Monitor',
            labels={'left': 'Channel'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )

        self.stream_scroll.setYRange(-4,4,padding=.01)

        # self.stream_scroll.setXRange(0,100, padding=.01)
        self.stream_scroll.setXRange(timestamp(), timestamp() + 100)

        self.layout = QtGui.QGridLayout()
        self.stream_scroll.plotItem.showGrid(True, True, .5)
        self.layout.addWidget(self.stream_scroll,0,0)

        C=pg.hsvColor(.7,alpha=.5)
        self.pen=pg.mkPen(color=C,width=1)
        self.curve = self.stream_scroll.plot(pen=self.pen)

    def update1(self):
        # global data
        if len(self.data) > 100:
            self.data[:-1] = self.data[1:] # shift data in the array one, see also np.pull
            self.data[-1] = np.random.rand() # .normal()
            self.Xtime[:-1] = self.Xtime[1:]
            self.Xtime[-1] = timestamp() # int(round(time.time()*1000))+100
            self.TimerFirstRun = False

        else:
            self.data.append(np.random.rand())
            self.Xtime.append(timestamp())

        X = self.Xtime
        # Y=np.sin(np.arange(points)/points*3*np.pi+time.time()) # draw sin wave
        Y = self.data  # np.random.rand(100)
        self.curve.setData(X, Y)

    def ticker(self):
        if self.RNDbtn == False:
            self.timer = pg.QtCore.QTimer()
            self.timer.timeout.connect(self.update1)
            self.timer.start(self.refreshInterval)
            self.RNDbtn = True
            self.GetDataBtn.setStyleSheet("background-color: green")
            self.GetDataBtn.setText("Disconnect")

        else:
            self.timer.stop()
            self.RNDbtn = False
            self.GetDataBtn.setStyleSheet("background-color: red")
            self.GetDataBtn.setText("Connect")



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = WindowPlot()
    sys.exit(App.exec())
