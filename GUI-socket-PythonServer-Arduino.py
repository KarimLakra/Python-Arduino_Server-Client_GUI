import sys, os, signal, socket, subprocess, netifaces, random, time, traceback
from datetime import datetime

from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton,
    QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QBoxLayout, QLayout,
    QDialogButtonBox, QListView, QLineEdit, QScrollArea, QWidget,
    QSlider, QGridLayout)
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QRect, Qt, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt as QTC

import pyqtgraph as pg
import numpy as np

from XAxisTime import TimeAxisItem, timestamp
import getIP_List_func

ServerStatus = False    # global server status
DataBuffer = [] # global Data received from socket

class DigitalIN_OUT(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        self.InitLEDS()
        vbox.addWidget(self.groupBoxLEDS)
        self.setLayout(vbox)


    def InitLEDS(self):
        hboxlayoutLEDS = QHBoxLayout()
        # hboxlayout.setSizeConstraint(QLayout.SetFixedSize)
        self.groupBoxLEDS = QGroupBox("Digital Inputs/Outputs")

        self.GridDigiIO = QtWidgets.QGridLayout()

        self.DigiIO2 = QtWidgets.QPushButton("D2")
        self.DigiIO2.setEnabled(False)
        self.DigiIO2.setMaximumHeight(40)
        self.DigiIO2.setMaximumWidth(40)
        self.GridDigiIO.addWidget(self.DigiIO2, 0, 0)

        self.DigiIO3 = QtWidgets.QPushButton("D3")
        self.DigiIO3.setEnabled(False)
        self.DigiIO3.setMaximumHeight(40)
        self.DigiIO3.setMaximumWidth(40)
        self.GridDigiIO.addWidget(self.DigiIO3, 0, 1)

        self.DigiIO4 = QtWidgets.QPushButton("D4")
        self.DigiIO4.setEnabled(False)
        self.DigiIO4.setMaximumHeight(40)
        self.DigiIO4.setMaximumWidth(40)
        self.GridDigiIO.addWidget(self.DigiIO4, 1, 0)

        self.DigiIO5 = QtWidgets.QPushButton("D5")
        self.DigiIO5.setObjectName("New")
        self.DigiIO5.setEnabled(False)
        self.DigiIO5.setMaximumHeight(40)
        self.DigiIO5.setMaximumWidth(40)
        self.DigiIO5.clicked.connect(self.updateLED)
        self.GridDigiIO.addWidget(self.DigiIO5, 1, 1)

        hboxlayoutLEDS.addLayout(self.GridDigiIO)
        self.groupBoxLEDS.setLayout(hboxlayoutLEDS)


    def updateLED(self):
        self.DigiIO5.setStyleSheet("background-color: green")
        # global ServerStatus, DataBuffer
        # stat_D5 = int(DataBuffer[7][2])
        # if stat_D5 == 1:
        #     print('High')
        #     self.DigiIO5.setStyleSheet("background-color: green")
        # else:
        #     print('Low')
        #     self.DigiIO5.setStyleSheet("background-color: red")




class WindowPlot(QMainWindow):
    def __init__(self, parent=None):
        pg.setConfigOption('background', 'w') #before loading widget
        super(WindowPlot, self).__init__(parent)

        self.ReadDbtn = False
        self.Buffer_AnalogA0 = [] #np.random.normal(size=100)
        self.Buffer_AnalogA1 = []
        self.Buffer_AnalogA2 = []
        self.Buffer_AnalogA3 = []
        self.Buffer_D2 = []
        self.Buffer_D3 = []
        self.Buffer_D4 = []
        self.Buffer_D5 = []


        self.Xtime = []
        self.refreshInterval = 1000 # default refresh plot every 1s
        self.timer = pg.QtCore.QTimer()
        self.errReadEvent = ''  # holds error history
        self.counterTest = 0

        self.wid = QtGui.QWidget(self)
        self.setCentralWidget(self.wid)

        vbox = QVBoxLayout()
        self.InitLEDS()
        self.createLayout1()
        vbox.addWidget(self.groupBoxLEDS)
        vbox.addWidget(self.groupBoxPlot)
        vbox.addWidget(self.groupBoxData)
        self.wid.setLayout(vbox)


    def InitLEDS(self):
        hboxlayoutLEDS = QHBoxLayout()
        # hboxlayout.setSizeConstraint(QLayout.SetFixedSize)
        self.groupBoxLEDS = QGroupBox("Digital Inputs/Outputs")

        self.GridDigiIO = QtWidgets.QGridLayout()

        self.DigiIO2 = QtWidgets.QPushButton("D2")
        self.DigiIO2.setEnabled(False)
        self.DigiIO2.setMaximumHeight(40)
        self.DigiIO2.setMaximumWidth(40)
        self.GridDigiIO.addWidget(self.DigiIO2, 0, 0)

        self.DigiIO3 = QtWidgets.QPushButton("D3")
        self.DigiIO3.setEnabled(False)
        self.DigiIO3.setMaximumHeight(40)
        self.DigiIO3.setMaximumWidth(40)
        self.GridDigiIO.addWidget(self.DigiIO3, 0, 1)

        self.DigiIO4 = QtWidgets.QPushButton("D4")
        self.DigiIO4.setEnabled(False)
        self.DigiIO4.setMaximumHeight(40)
        self.DigiIO4.setMaximumWidth(40)
        self.GridDigiIO.addWidget(self.DigiIO4, 1, 0)

        self.DigiIO5 = QtWidgets.QPushButton("D5")
        self.DigiIO5.setObjectName("New")
        self.DigiIO5.setEnabled(False)
        self.DigiIO5.setMaximumHeight(40)
        self.DigiIO5.setMaximumWidth(40)
        self.GridDigiIO.addWidget(self.DigiIO5, 1, 1)

        hboxlayoutLEDS.addLayout(self.GridDigiIO)
        self.groupBoxLEDS.setLayout(hboxlayoutLEDS)


    def createLayout1(self):
        vboxlayoutPlot = QVBoxLayout()
        vboxlayoutData = QVBoxLayout()
        self.groupBoxPlot = QGroupBox("Plotting")
        self.groupBoxData = QGroupBox("Data")
        self.create_plot()
        vboxlayoutPlot.addLayout(self.layout)

        self.gridPlot = QGridLayout()
        self.gridData = QGridLayout()

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
        self.cb.addItems(["5", "2", "1"])
        self.cb.setCurrentIndex(2)
        self.cb.currentIndexChanged.connect(self.ComboInterval)

        self.Refr = QHBoxLayout()
        self.labelInterval = QLabel()
        self.labelInterval.setText("Refresh rate (s)")

        self.Refr.addWidget(self.labelInterval)
        self.Refr.addWidget(self.cb)

        # Error box START
        self.hboxErrSourceDt = QHBoxLayout()
        self.ErrorGroup = QGroupBox("Errors")
        self.vboxErrBox = QVBoxLayout()
        self.hboxErrLEDLBL = QHBoxLayout()
        self.hboxErrorEvents = QHBoxLayout()
        self.hboxErrorEvents.setSizeConstraint(QLayout.SetFixedSize)

        self.LEDError = QPushButton()   # used as error LED indicator
        self.LEDError.setEnabled(False)
        self.LEDError.setMaximumHeight(15)
        self.LEDError.setMaximumWidth(15)

        self.labelErrorRead = QLabel()
        self.labelErrorRead.setText("Error reading data")

        self.label_ErrorReadEvents = QLabel()
        self.label_ErrorReadEvents.setFont(QtGui.QFont("Sanserif", 10))
        self.label_ErrorReadEvents.setMinimumWidth(200)

        scrollErrors = QScrollArea()
        scrollErrors.setWidget(self.label_ErrorReadEvents)
        scrollErrors.setWidgetResizable(True)
        # scrollErrors.setMaximumHeight(80)
        scrollErrors.setMinimumWidth(200)

        self.hboxErrLEDLBL.addWidget(self.LEDError)
        self.hboxErrLEDLBL.addWidget(self.labelErrorRead)
        self.vboxErrBox.addLayout(self.hboxErrLEDLBL)
        self.vboxErrBox.addWidget(scrollErrors)
        self.ErrorGroup.setLayout(self.vboxErrBox)

        self.cbDataSource = QtWidgets.QComboBox()
        # self.cb.addItem("10")
        self.cbDataSource.addItems(["Random generated test Data", "Remote data"])
        self.cbDataSource.setCurrentIndex(1)

        self.hboxErrSourceDt.addWidget(self.ErrorGroup)
        self.hboxErrSourceDt.addWidget(self.cbDataSource)
        # Error box END

        self.GetDataBtn = QPushButton("Start Plot")
        self.stream_scroll.enableAutoRange(enable=True) # move the plot to new data

        self.GetDataBtn.clicked.connect(self.ticker)
        self.GetDataBtn.setMinimumHeight(50)
        self.GetDataBtn.setMinimumWidth(180)

        self.gridPlot.addWidget(self.slider, 0, 0)
        self.gridPlot.addLayout(self.Refr, 1, 0)

        self.gridData.addLayout(self.hboxErrSourceDt, 0, 0)
        self.gridData.addWidget(self.GetDataBtn, 0, 1)

        vboxlayoutPlot.addLayout(self.gridPlot)
        self.groupBoxPlot.setLayout(vboxlayoutPlot)

        vboxlayoutData.addLayout(self.gridData)
        self.groupBoxData.setLayout(vboxlayoutData)

    # def SliderVal(self):
    #     print(self.slider.value())


    def ComboInterval(self):
        self.refreshInterval = int(self.cb.currentText())*1000
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(self.refreshInterval)

    def create_plot(self):
        self.stream_scroll = pg.PlotWidget(
            title='Stream Monitor',
            labels={'left': 'Channel'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )
        self.stream_scroll.setMinimumHeight(200)
        self.stream_scroll.setYRange(-4,4,padding=.01)

        # self.stream_scroll.setXRange(0,100, padding=.01)
        self.stream_scroll.setXRange(timestamp(), timestamp() + 100)

        self.layout = QtGui.QGridLayout()
        self.stream_scroll.plotItem.showGrid(True, True, .5)
        self.layout.addWidget(self.stream_scroll,0,0)

        C=pg.hsvColor(.7,alpha=.5)
        self.pen=pg.mkPen(color=C,width=1)
        self.curve = self.stream_scroll.plot(pen=self.pen)

        C1=pg.hsvColor(.6,alpha=.5)
        self.pen1=pg.mkPen(color=C1,width=1)
        self.curve1 = self.stream_scroll.plot(pen=self.pen1)

        C2=pg.hsvColor(.5,alpha=.5)
        self.pen2=pg.mkPen(color=C2,width=1)
        self.curve2 = self.stream_scroll.plot(pen=self.pen2)

        C3=pg.hsvColor(.4,alpha=.5)
        self.pen3=pg.mkPen(color=C3,width=1)
        self.curve3 = self.stream_scroll.plot(pen=self.pen3)


    def updatePlot(self):
        global ServerStatus, DataBuffer
        # Plot only if data is available, else stop and switch button off
        if ServerStatus == True or self.cbDataSource.currentIndex() == 0:
            # data format [['A0', 'I', '703'], ['A1', 'I', '55'], ['A2', 'I', '56'], ['A3', 'I', '57'], ['D2', 'I', '1'], ['D3', 'I', '1'], ['D4', 'I', '0'], ['D5', 'I', '1']]
            DataBuffer = self.FiledataConvert()

            if not len((DataBuffer)[0][0])==0:
                # if buffer reading success continue, else escape to next
                # data to prevent the script from stopping

                if int(DataBuffer[4][2])==1:
                    self.DigiIO2.setStyleSheet("background-color: green") # update DigiIO for digital IO
                else:
                    self.DigiIO2.setStyleSheet("background-color: red")

                if int(DataBuffer[5][2])==1:
                    self.DigiIO3.setStyleSheet("background-color: green")
                else:
                    self.DigiIO3.setStyleSheet("background-color: red")

                if int(DataBuffer[6][2])==1:
                    self.DigiIO4.setStyleSheet("background-color: green")
                else:
                    self.DigiIO4.setStyleSheet("background-color: red")

                if int(DataBuffer[7][2])==1:
                    self.DigiIO5.setStyleSheet("background-color: green")
                else:
                    self.DigiIO5.setStyleSheet("background-color: red")

                def readAnalog(indx):
                    a = DataBuffer[indx][2]
                    b = DataBuffer[indx][0]
                    a = round(int(a)/204, 3)
                    return a, b

                # check if buffer size is 100, start to empty old and append new, else append to buffer
                if len(self.Buffer_AnalogA0) > 100:
                    self.Buffer_AnalogA0[:-1] = self.Buffer_AnalogA0[1:] # shift data in the array one, see also np.pull
                    self.Buffer_AnalogA1[:-1] = self.Buffer_AnalogA1[1:]
                    self.Buffer_AnalogA2[:-1] = self.Buffer_AnalogA2[1:]
                    self.Buffer_AnalogA3[:-1] = self.Buffer_AnalogA3[1:]

                    if self.cbDataSource.currentIndex() == 0:
                        self.Buffer_AnalogA0[-1] = np.random.randint(20) # .normal()
                    else:
                        a0 = readAnalog(0)[0]
                        self.Buffer_AnalogA0[-1] = a0
                        a1 = readAnalog(1)[0]
                        self.Buffer_AnalogA1[-1] = a1
                        a2 = readAnalog(2)[0]
                        self.Buffer_AnalogA2[-1] = a2
                        a3 = readAnalog(3)[0]
                        self.Buffer_AnalogA3[-1] = a3

                    self.Xtime[:-1] = self.Xtime[1:]
                    self.Xtime[-1] = timestamp()

                else:
                    if self.cbDataSource.currentIndex() == 0:
                        # self.data.append(np.random.rand())
                        self.Buffer_AnalogA0.append(np.random.randint(20))
                    else:
                        a0 = readAnalog(0)[0]
                        # print(readAnalog(0)[1])   # channel name A0
                        # print(readAnalog(0)[2])   # input/output: I
                        self.Buffer_AnalogA0.append(a0)
                        a1 = readAnalog(1)[0]
                        self.Buffer_AnalogA1.append(a1)
                        a2 = readAnalog(2)[0]
                        self.Buffer_AnalogA2.append(a2)
                        a3 = readAnalog(3)[0]
                        self.Buffer_AnalogA3.append(a3)

                    self.Xtime.append(timestamp())

                X = self.Xtime
                # Y=np.sin(np.arange(points)/points*3*np.pi+time.time()) # draw sin wave
                Y0 = self.Buffer_AnalogA0  # np.random.rand(100)
                Y1 = self.Buffer_AnalogA1
                Y2 = self.Buffer_AnalogA2
                Y3 = self.Buffer_AnalogA3
                # Plot data
                self.curve.setData(X, Y0)
                self.curve1.setData(X, Y1)
                self.curve2.setData(X, Y2)
                self.curve3.setData(X, Y3)
            else:
                datetimeObj = datetime.now()
                self.LEDError.setStyleSheet("background-color: red")
                errmsg = 'Error reading Buffer at:' +  str(datetimeObj)
                self.errReadEvent = self.errReadEvent + errmsg + '\n'
                self.label_ErrorReadEvents.setText(self.errReadEvent)
                print(errmsg)


        else:
            self.timer.stop()
            self.ReadDbtn = False
            self.GetDataBtn.setStyleSheet("background-color: red")
            self.GetDataBtn.setText("Start Plot")

    def FiledataConvert(self):
        def rdf():
            f = open("output1.txt", "r")
            dt = f.read()
            f.close()
            dt = dt.split("-")
            for index, line in enumerate(dt):
                dt[index] = line.split(':')
            return dt

        a = rdf()
        # if len((a)[0][0])==0:
        #     datetimeObj = datetime.now()
        #     print('Error at :' + str(datetimeObj))
        #     self.LEDError.setStyleSheet("background-color: red")
        #     self.errReadEvent = self.errReadEvent + 'Error reading Data at:' +  str(datetimeObj) + '\n'
        #     self.label_ErrorReadEvents.setText(self.errReadEvent)
        #     time.sleep(3)
        #     a = rdf()
        # a = round(int(a)/204, 3)
        self.LEDError.setStyleSheet("background-color: blue")
        return a


    def ticker(self):
        datetimeObj = datetime.now()
        global ServerStatus
        if (self.ReadDbtn == False and ServerStatus == True) or (self.ReadDbtn == False and self.cbDataSource.currentIndex() == 0):
            # DEBUG_ print time reading data started
            print('Reading started at : ' + str(datetimeObj))

            self.timer = pg.QtCore.QTimer()
            self.timer.timeout.connect(self.updatePlot)
            self.timer.start(self.refreshInterval)
            self.ReadDbtn = True
            self.GetDataBtn.setStyleSheet("background-color: green")
            self.GetDataBtn.setText("Stop Plot")

        elif (self.ReadDbtn == True and ServerStatus == True) or (self.ReadDbtn == True and self.cbDataSource.currentIndex() == 0):
            print('Reading stopped at : ' + str(datetimeObj))
            self.timer.stop()
            self.ReadDbtn = False
            self.GetDataBtn.setStyleSheet("background-color: red")
            self.GetDataBtn.setText("Start Plot")

class Main_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.RNDbtn = False
        self.InitWindow()


    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("Socket Server")
        self.setGeometry(500, 50, 800, 800)

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
        vboxlayout_plt = QVBoxLayout()
        # hboxPLT = QHBoxLayout()
        self.groupBox_Plt = QGroupBox("Data")

        # DigiInOut = DigitalIN_OUT()
        plotD = WindowPlot()

        # vboxlayout_plt.addWidget(DigiInOut)
        vboxlayout_plt.addWidget(plotD)
        # hboxlayout_plt.addStretch()
        self.groupBox_Plt.setLayout(vboxlayout_plt)


    def createLyt_ServerEvents(self):
        self.hboxlayout_serverE = QHBoxLayout()
        self.hboxlayout_serverE.setSizeConstraint(QLayout.SetFixedSize)
        self.groupBox_servE = QGroupBox("Server events")

        self.label_servE = QLabel()
        self.label_servE.setFont(QtGui.QFont("Sanserif", 10))
        # self.label_servE.setMaximumHeight(80)
        self.label_servE.setMinimumWidth(790)

        scroll = QScrollArea()
        scroll.setWidget(self.label_servE)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(80)
        scroll.setMinimumWidth(800)
        self.hboxlayout_serverE.addWidget(scroll)


        self.groupBox_servE.setLayout(self.hboxlayout_serverE)


    def ChooseIP(self):
        dlg = getIP_List_func.FindAdapter(self)
        if dlg.exec_():
            # print(dlg.IPselected)
            # self.label.setText(dlg.IPselected)
            self.IPSel = dlg.IPselected
            self.ServerIP.setText(self.IPSel)

    def SConnect(self):
        global ServerStatus
        ServerStatus = True
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
        global ServerStatus
        ServerStatus = False
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
