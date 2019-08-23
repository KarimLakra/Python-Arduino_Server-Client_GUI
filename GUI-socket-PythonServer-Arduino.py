from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QDialog, \
QGroupBox, QHBoxLayout, QVBoxLayout, QBoxLayout, QDialogButtonBox, QListView, QLineEdit
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import sys
import os
import socket
import subprocess
import netifaces
import getIP_List_func

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("Server control")
        self.setGeometry(500, 200, 300, 250)

        self.createLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)

        self.ServerIP = QLineEdit(self)
        # self.ServerIP.move(20,20)
        self.ServerIP.resize(280,40)
        vbox.addWidget(self.ServerIP)

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

    def createLayout(self):
        self.groupBox = QGroupBox("Python Socket server - Arduino")

        hboxlayout = QHBoxLayout()

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


    def ChooseIP(self):
        dlg = getIP_List_func.CustomDialog(self)
        if dlg.exec_():
            # print(dlg.IPselected)
            self.label.setText(dlg.IPselected)
        # else:
        #     print("Cancel!")


    def SConnect(self):
        print("Server is running")
        with open('output.txt', 'w') as f:
            self.p = subprocess.Popen(["python", "-u", "ArduinoSocket.py"], stdout = f)

    def SDisconnect(self):
        self.p.terminate()
        print("Server Disconnected")


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
