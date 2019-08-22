from PyQt5.QtWidgets import QMainWindow, QApplication, QGroupBox, QPushButton, QHBoxLayout, QVBoxLayout, QBoxLayout, QListView, QDialog
import sys
import os
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import subprocess
import socket
import netifaces

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.init_widget()


    def init_widget(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("Select Ip address")
        self.setGeometry(500, 200, 500, 200)

        widget_laytout = QBoxLayout(QBoxLayout.LeftToRight)

        group = QGroupBox()
        box = QBoxLayout(QBoxLayout.TopToBottom)
        group.setLayout(box)
        group.setTitle("Adapters list")
        widget_laytout.addWidget(group)

        fruits = ["Buttons in GroupBox", "TextBox in GroupBox", "Label in GroupBox", "TextEdit"]
        view = QListView(self)
        self.model = QStandardItemModel()

        # for f in fruits:
        #     model.appendRow(QStandardItem(f))
        self.listAddrs()

        view.setModel(self.model)
        box.addWidget(view)
        stk_w = QVBoxLayout()
        self.setLayout(widget_laytout)

        self.show()

    def listAddrs(self):
        ad = netifaces.interfaces()
        for adpt in ad:
            # print(netifaces.ifaddresses(adpt))
            va = netifaces.ifaddresses(adpt)
            if 2 in va:
                adapt = netifaces.ifaddresses(adpt)[2][0] # ['addr']
                # print(adapt)
                self.model.appendRow(QStandardItem('addr: ' + adapt['addr'] +
                '  netmask: ' + adapt['netmask'] +
                '  broadcast: ' + adapt['broadcast']))



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
