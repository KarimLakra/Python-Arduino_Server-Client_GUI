from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, QDialog,
QGroupBox, QHBoxLayout, QVBoxLayout, QBoxLayout, QDialogButtonBox, QListView, QLineEdit)
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import sys
import os
import signal
import socket
import subprocess
import netifaces
import getIP_List_func

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.InitWindow()

        # self.IPSel = ''
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("Socket Server")
        self.setGeometry(500, 200, 300, 250)

        self.createLayout1()
        self.createLayout2()

        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        vbox.addWidget(self.groupBox1)

        self.label = QLabel(self)
        self.label.setFont(QtGui.QFont("Sanserif", 15))
        vbox.addWidget(self.label)

        buttonSerachAdapter = QPushButton("Search Network Adapters", self)
        buttonSerachAdapter.setIconSize(QtCore.QSize(40,40))
        buttonSerachAdapter.setMinimumHeight(40)
        buttonSerachAdapter.clicked.connect(self.ChooseIP)
        # buttonSerachAdapter.clicked.connect(self.IPADD)
        vbox.addWidget(buttonSerachAdapter)

        self.setLayout(vbox)
        self.show()

    def createLayout1(self):
        hboxlayout = QHBoxLayout()
        self.groupBox = QGroupBox("Python Socket server - Arduino")

        button = QPushButton("Run server", self)
        button.setIcon(QtGui.QIcon("StartServer.png"))
        button.setIconSize(QtCore.QSize(40,40))
        button.setToolTip("<h2>Run</h2>the server")    #tooltip with HTML tag
        button.setMinimumHeight(40)
        button.clicked.connect(self.SConnect)
        hboxlayout.addWidget(button)

        button1 = QPushButton("Stop server", self)
        button1.setIcon(QtGui.QIcon("StopServer.png"))
        button1.setIconSize(QtCore.QSize(40,40))
        button1.setToolTip("<h2>Stop</h2> the server")
        button1.setMinimumHeight(40)
        button1.clicked.connect(self.SDisconnect)
        hboxlayout.addWidget(button1)

        button2 = QPushButton("Quit", self)
        button2.setIcon(QtGui.QIcon("Quit.png"))
        button2.setIconSize(QtCore.QSize(40,40))
        button2.setToolTip("<h2>Quit</h2> this application")
        button2.setMinimumHeight(40)
        button2.clicked.connect(lambda : sys.exit())
        hboxlayout.addWidget(button2)

        self.groupBox.setLayout(hboxlayout)

    def createLayout2(self):
        vboxIP_Port = QVBoxLayout()
        hboxIP = QHBoxLayout()
        hboxPort = QHBoxLayout()

        self.groupBox1 = QGroupBox("IP && Port:")

        self.label0 = QLabel(self)
        self.label0.setText("Server IP:")
        self.ServerIP = QLineEdit(self)
        self.ServerIP.setFixedWidth(200)
        self.ServerIP.setText('192.168.1.2')
        # hboxIP.addWidget(self.label0, Qt.AlignLeft)
        hboxIP.addWidget(self.label0)
        hboxIP.addWidget(self.ServerIP)
        hboxIP.addStretch(1)

        self.label1 = QLabel(self)
        self.label1.setText("Port:")
        self.PortN = QLineEdit(self)
        self.PortN.setFixedWidth(100)
        self.PortN.setText('65432')
        hboxPort.addWidget(self.label1)
        hboxPort.addWidget(self.PortN)
        hboxPort.addStretch(1)

        vboxIP_Port.addLayout(hboxIP)
        vboxIP_Port.addLayout(hboxPort)

        self.groupBox1.setLayout(vboxIP_Port)

    def ChooseIP(self):
        dlg = getIP_List_func.CustomDialog(self)
        if dlg.exec_():
            # print(dlg.IPselected)
            # self.label.setText(dlg.IPselected)
            self.IPSel = dlg.IPselected
            self.ServerIP.setText(self.IPSel)
        # else:
        #     print("Cancel!")


    def SConnect(self):
        print("Server is running")
        # with open('output.txt', 'w') as f:
            # self.p = subprocess.Popen(["python", "-u", "ArduinoSocket.py","name1","name2","name3"] , stdout = f)
        ipServ = self.ServerIP.text()
        portN = self.PortN.text()

        self.p = subprocess.Popen(["python", "-u", "ArduinoSocket.py", ipServ, portN] , shell = True)

    def SDisconnect(self):
        cmd = 'for /f "tokens=5" %a in (\'netstat -aon ^| find "65432"\') do taskkill /f /pid %a'
        os.system(cmd)
        print("Server Disconnected")


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
