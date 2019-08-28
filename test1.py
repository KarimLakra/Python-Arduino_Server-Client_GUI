# https://www.swharden.com/wp/page/5/

import sys, time, random
from PyQt5.QtWidgets import (QMainWindow,QApplication,QDialog,
QHBoxLayout, QVBoxLayout, QGroupBox, QWidget, QPushButton)
from PyQt5 import QtGui
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


class WindowPlot(QMainWindow):
    def __init__(self, parent=None):
        pg.setConfigOption('background', 'w') #before loading widget
        super(WindowPlot, self).__init__(parent)

        self.RNDbtn = False

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

        self.GetDataBtn = QPushButton("Connect")
        self.GetDataBtn.clicked.connect(self.ticker)
        self.GetDataBtn.setMinimumHeight(50)
        self.GetDataBtn.setMinimumWidth(180)
        vboxlayout.addWidget(self.GetDataBtn)

        self.groupBox.setLayout(vboxlayout)


    def create_plot(self):

        self.stream_scroll = pg.PlotWidget(title='Stream Monitor')

        # if not self.parent.daisy_entry.currentIndex():
        self.channel_count = 16
        self.buffer_size = 1000
        samples = 125
        self.stream_scroll.setYRange(-.5,16,padding=.01)
        # else:
        # self.channel_count = 8
        #   samples = 250
        #   self.buffer_size = 2000
        #   self.stream_scroll.setYRange(-.5,8,padding=.01)

        # self.stream_scroll_time_axis = np.linspace(-5,0,samples)
        self.stream_scroll.setXRange(-5,0, padding=.01)
        self.stream_scroll.setLabel('bottom','Time','Seconds')
        self.stream_scroll.setLabel('left','Channel')
        # for i in range(self.channel_count-1,-1,-1):
        #   self.data_buffer['buffer_channel{}'.format(i+1)] = deque([0]*self.buffer_size)
        #   self.filtered_data['filtered_channel{}'.format(i+1)] = deque([0]*samples)
        #   self.curves['curve_channel{}'.format(i+1)] = self.stream_scroll.plot()
        #   self.curves['curve_channel{}'.format(i+1)].setData(x=self.stream_scroll_time_axis,y=([point+i+1 for point in self.filtered_data['filtered_channel{}'.format(i+1)]]))
        self.layout = QtGui.QGridLayout()
        self.stream_scroll.plotItem.showGrid(True, True, 0.7)
        self.layout.addWidget(self.stream_scroll,0,0)

    def update1(self):
        t1=time.process_time()
        points=100 #number of data points
        X=np.arange(points)
        # Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        Y=np.random.rand(100)
        # C=pg.hsvColor(time.time()/5%1,alpha=.5) # Change color each tick
        C=pg.hsvColor(0,alpha=.5)
        pen=pg.mkPen(color=C,width=1)
        self.stream_scroll.plot(X,Y,pen=pen,clear=True)
        print("update took %.02f ms"%((time.process_time()-t1)*1000))
        # if self.chkMore.isChecked():
        #     QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

    def ticker(self):
        if self.RNDbtn == False:
            self.timer = pg.QtCore.QTimer()
            self.timer.timeout.connect(self.update1)
            self.timer.start(1000)
            print('started')
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
