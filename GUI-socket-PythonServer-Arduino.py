import sys, os, signal, socket, subprocess, netifaces, random, getIP_List_func, time

from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton,
    QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QBoxLayout, QLayout,
    QDialogButtonBox, QListView, QLineEdit, QScrollArea, QWidget, QGridLayout)
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QRect, Qt, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import pyqtgraph as pg
import numpy as np

import matplotlib
matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # uic.loadUi('test.ui', self)
#         self.content_plot = QWidget(self)
#         self.content_plot.resize(800, 350)
#         self.content_plot.move(0,0)
#
#         # test data
#         data = np.array([0.7,0.7,0.7,0.8,0.9,0.9,1.5,1.5,1.5,1.5])
#         fig, ax1 = plt.subplots()
#         bins = np.arange(0.6, 1.62, 0.02)
#         n1, bins1, patches1 = ax1.hist(data, bins, alpha=0.6, density=False, cumulative=False)
#         # plot
#         self.plotWidget = FigureCanvas(fig)
#         # lay = QtWidgets.QVBoxLayout(self.content_plot)
#         lay = QtWidgets.QVBoxLayout(self.content_plot)
#         lay.setContentsMargins(0, 0, 0, 0)
#         lay.addWidget(self.plotWidget)
#         # add toolbar
#         self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.plotWidget, self))

class WindowPlot(QMainWindow):
    def __init__(self, parent=None):
        # pg.setConfigOption('background', 'w') #before loading widget
        super(WindowPlot, self).__init__(parent)

        self.RNDbtn = False
        self.data = np.random.normal(size=100)
        self.refreshInterval = 1000 # refresh plot every 1s
        self.timer = pg.QtCore.QTimer()

        self.wid = QtGui.QWidget(self)
        self.setCentralWidget(self.wid)

        vbox = QVBoxLayout()
        self.createLayout1()
        vbox.addWidget(self.groupBox)
        self.wid.setLayout(vbox)

        # self.show()

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

        # self.slider = QSlider(QTC.Horizontal)
        # self.slider.setFocusPolicy(QTC.StrongFocus)
        # self.slider.setTickPosition(QSlider.TicksBothSides)
        # self.slider.setTickInterval(1)
        # self.slider.setSingleStep(1)
        # self.slider.setMaximum(10)
        # self.slider.setMinimum(0)
        # self.slider.valueChanged.connect(self.SliderVal)
        # self.slider.setValue(7)

        self.cb = QtWidgets.QComboBox()
        # self.cb.addItem("10")
        self.cb.addItems(["1000", "500", "250", "100", "50"])
        self.cb.currentIndexChanged.connect(self.ComboInterval)

        # self.grid.addWidget(self.slider, 0, 0)
        self.grid.addWidget(self.GetDataBtn, 0, 0)
        self.grid.addWidget(self.cb, 0, 1)


        vboxlayout.addLayout(self.grid)
        self.groupBox.setLayout(vboxlayout)

    def SliderVal(self):
        print(self.slider.value())
    def ComboInterval(self):
        self.refreshInterval = int(self.cb.currentText())
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(self.refreshInterval)


    def create_plot(self):

        self.stream_scroll = pg.PlotWidget(title='Stream Monitor')

        # if not self.parent.daisy_entry.currentIndex():
        # self.channel_count = 16
        # self.buffer_size = 1000
        # samples = 125
        self.stream_scroll.setYRange(-4,4,padding=.01)
        # else:
        # self.channel_count = 8
        #   samples = 250
        #   self.buffer_size = 2000
        #   self.stream_scroll.setYRange(-.5,8,padding=.01)

        # self.stream_scroll_time_axis = np.linspace(-5,0,samples)
        self.stream_scroll.setXRange(0,100, padding=.01)
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
        self.data[:-1] = self.data[1:] # shift data in the array one, see also np.pull
        self.data[-1] = np.random.normal()
        t1=time.process_time()
        points=100 #number of data points
        X=np.arange(points)
        # Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        Y=self.data  # np.random.rand(100)
        # C=pg.hsvColor(time.time()/5%1,alpha=.5) # Change color each tick
        C=pg.hsvColor(0.7,alpha=.5)
        pen=pg.mkPen(color=C,width=1)
        self.stream_scroll.plot(X,Y,pen=pen,clear=True)
        print("update took %.02f ms"%((time.process_time()-t1)*1000))
        # if self.chkMore.isChecked():
        #     QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

    def ticker(self):
        if self.RNDbtn == False:
            # self.timer = pg.QtCore.QTimer()
            self.timer.timeout.connect(self.update1)
            self.timer.start(self.refreshInterval)
            print('started')
            self.RNDbtn = True
            self.GetDataBtn.setStyleSheet("background-color: green")
            self.GetDataBtn.setText("Disconnect")
        else:
            self.timer.stop()
            self.RNDbtn = False
            self.GetDataBtn.setStyleSheet("background-color: red")
            self.GetDataBtn.setText("Connect")

class Main_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.RNDbtn = False
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("Socket Server")
        self.setGeometry(500, 200, 800, 800)

        self.createLayout1()
        self.createLayout2()
        self.CreateLyt_plotData(QMainWindow)
        self.createLyt_ServerEvents()

        vbox = QVBoxLayout()
        hboxPort_debugLbl = QHBoxLayout()

        hboxPort_debugLbl.addWidget(self.groupBox1)
        hboxPort_debugLbl.addWidget(self.groupBox2)

        vbox.addWidget(self.groupBox)
        vbox.addLayout(hboxPort_debugLbl)
        vbox.addWidget(self.groupBox_Plt)
        vbox.addWidget(self.groupBox_servE)

        self.setLayout(vbox)

        self.show()

    def createLayout1(self):
        hboxlayout = QHBoxLayout()
        # hboxlayout.setSizeConstraint(QLayout.SetFixedSize)
        self.groupBox = QGroupBox("Python Socket server - Arduino")

        hboxlayout.addStretch(1)
        button = QPushButton("Run server")
        button.setIcon(QtGui.QIcon("StartServer.png"))
        button.setIconSize(QtCore.QSize(40,40))
        button.setToolTip("<h2>Run</h2>the server")    #tooltip with HTML tag
        button.setMinimumHeight(50)
        button.setMinimumWidth(120)
        button.clicked.connect(self.SConnect)
        hboxlayout.addWidget(button)
        hboxlayout.addStretch(1)

        button1 = QPushButton("Stop server")
        button1.setIcon(QtGui.QIcon("StopServer.png"))
        button1.setIconSize(QtCore.QSize(40,40))
        button1.setToolTip("<h2>Stop</h2> the server")
        button1.setMinimumHeight(50)
        button1.setMinimumWidth(120)
        button1.clicked.connect(self.SDisconnect)
        hboxlayout.addWidget(button1)
        hboxlayout.addStretch(1)

        button2 = QPushButton("Quit")
        button2.setIcon(QtGui.QIcon("Quit.png"))
        button2.setIconSize(QtCore.QSize(40,40))
        button2.setToolTip("<h2>Quit</h2> this application")
        button2.setMinimumHeight(50)
        button2.setMinimumWidth(120)
        button2.clicked.connect(lambda : sys.exit())
        hboxlayout.addWidget(button2)
        hboxlayout.addStretch(1)

        self.groupBox.setLayout(hboxlayout)

    def createLayout2(self):
        hboxLbl_Inp_But = QHBoxLayout()
        hboxLbl_Inp = QHBoxLayout()
        vboxLbls = QVBoxLayout()
        vboxInpts = QVBoxLayout()
        vboxSearchButton = QVBoxLayout()
        hboxDebug = QHBoxLayout()

        hboxLbl_Inp_But.setSizeConstraint(QLayout.SetFixedSize)

        self.groupBox1 = QGroupBox("IP && Port:")
        self.groupBox2 = QGroupBox("Debug:")

        self.label0 = QLabel(self)
        self.label0.setText("Server IP:")
        self.label1 = QLabel(self)
        self.label1.setText("Port:")
        self.label1.setMaximumHeight(50)

        vboxLbls.addWidget(self.label0)
        vboxLbls.addWidget(self.label1)

        self.ServerIP = QLineEdit(self)
        self.ServerIP.setFixedWidth(100)
        self.ServerIP.setText('192.168.1.2')

        self.PortN = QLineEdit(self)
        self.PortN.setFixedWidth(100)
        self.PortN.setText('65432')

        vboxInpts.addWidget(self.ServerIP)
        vboxInpts.addWidget(self.PortN)

        hboxLbl_Inp.addLayout(vboxLbls)
        hboxLbl_Inp.addLayout(vboxInpts)

        vboxSearchButton.addStretch(1)
        buttonSerachAdapter = QPushButton("Search Network Adapters", self)
        buttonSerachAdapter.setIcon(QtGui.QIcon("search_network.png"))
        buttonSerachAdapter.setMinimumHeight(50)
        buttonSerachAdapter.setMinimumWidth(180)
        buttonSerachAdapter.clicked.connect(self.ChooseIP)

        vboxSearchButton.addWidget(buttonSerachAdapter)
        vboxSearchButton.addStretch(1)

        hboxLbl_Inp_But.addLayout(hboxLbl_Inp)
        hboxLbl_Inp_But.addLayout(vboxSearchButton)

        self.labelDebug = QLabel(self)
        self.labelDebug.setText("Debug")

        self.buttonDebug = QPushButton("RND", self)
        # self.buttonDebug.setIcon(QtGui.QIcon("search_network.png"))
        self.buttonDebug.setMinimumHeight(50)
        self.buttonDebug.setMinimumWidth(180)
        self.buttonDebug.clicked.connect(self.startRandom)
        self.buttonDebug.setStyleSheet("background-color: red")

        hboxDebug.addWidget(self.labelDebug)
        hboxDebug.addWidget(self.buttonDebug)

        self.groupBox1.setLayout(hboxLbl_Inp_But)
        self.groupBox2.setLayout(hboxDebug)

    def CreateLyt_plotData(self, QMainWindow):
        hboxlayout_plt = QHBoxLayout()
        hboxPLT = QHBoxLayout()
        self.groupBox_Plt = QGroupBox("Received data")

        # plotD = MyWindow()
        plotD = WindowPlot()

        hboxlayout_plt.addWidget(plotD)
        # hboxlayout_plt.addStretch()
        self.groupBox_Plt.setLayout(hboxlayout_plt)


    def createLyt_ServerEvents(self):
        self.hboxlayout_serverE = QHBoxLayout()
        self.hboxlayout_serverE.setSizeConstraint(QLayout.SetFixedSize)
        self.groupBox_servE = QGroupBox("Server events")

        self.label_servE = QLabel()
        self.label_servE.setFont(QtGui.QFont("Sanserif", 10))
        self.label_servE.setMaximumHeight(80)
        self.label_servE.setMinimumWidth(790)

        scroll = QScrollArea()
        scroll.setWidget(self.label_servE)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(80)
        scroll.setMinimumWidth(800)
        self.hboxlayout_serverE.addWidget(scroll)


        self.groupBox_servE.setLayout(self.hboxlayout_serverE)


    def ChooseIP(self):
        dlg = getIP_List_func.CustomDialog(self)
        if dlg.exec_():
            # print(dlg.IPselected)
            # self.label.setText(dlg.IPselected)
            self.IPSel = dlg.IPselected
            self.ServerIP.setText(self.IPSel)

    def SConnect(self):
        print("Server is running")
        # with open('output.txt', 'w') as f:
            # self.p = subprocess.Popen(["python", "-u", "ArduinoSocket.py","name1","name2","name3"] , stdout = f)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Refresher)
        self.timer.start(100)

        ipServ = self.ServerIP.text()
        portN = self.PortN.text()
        with open('output.txt', 'w') as f:
            subprocess.Popen(["python", "-u", "ArduinoSocket.py", ipServ, portN] , stdout = f) # shell = True)

    def SDisconnect(self):
        cmd = 'for /f "tokens=5" %a in (\'netstat -aon ^| find "65432"\') do taskkill /t /f /pid %a'
        os.system(cmd)
        self.timer.stop()
        self.label_servE.setText("Server Disconnected")
        print("Server Disconnected")

    def Refresher(self):
        f = open("output.txt", "r")
        self.label_servE.setText(f.read())
        f.close()

    def startRandom(self):
        if self.RNDbtn == False:
            self.timerRND = QTimer(self)
            self.timerRND.timeout.connect(self.randomNum)
            self.timerRND.start(1000)
            self.RNDbtn = True
            self.buttonDebug.setStyleSheet("background-color: green")
        else:
            self.timerRND.stop()
            self.RNDbtn = False
            self.buttonDebug.setStyleSheet("background-color: red")

    def randomNum(self):
        rndN = random.randint(1,101)
        self.labelDebug.setText(str(rndN))


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Main_Window()
    sys.exit(App.exec())
