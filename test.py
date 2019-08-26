import sys
from PyQt5 import QtCore, QtWidgets,  QtGui
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QLabel, QPushButton,
    QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QBoxLayout,  QLayout,
    QDialogButtonBox, QListView, QLineEdit, QScrollArea)

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.t = False
        self.intw()

    def intw(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("Socket Server")
        self.setGeometry(500, 200, 700, 500)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        self.c = QWidget()
        self.c.setStyleSheet("background-color: red")
        self.c.setMaximumWidth(10)
        self.c.setMaximumHeight(10)
        self.c.move(30, 30)
        hbox.addWidget(self.c)
        # hbox.addStretch(0)

        button = QPushButton("Run server")
        button.setIcon(QtGui.QIcon("StartServer.png"))
        button.setIconSize(QtCore.QSize(40,40))
        button.setMinimumHeight(50)
        button.setMinimumWidth(120)
        button.clicked.connect(self.toogleColor)


        # hbox.addStretch(1)

        vbox.addLayout(hbox)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def toogleColor(self):
        if self.t == True:
            self.c.setStyleSheet("background-color: red")
            self.t = False
        else:
            self.c.setStyleSheet("background-color: green")
            self.t = True

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
