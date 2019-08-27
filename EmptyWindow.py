import sys
from PyQt5.QtWidgets import (QMainWindow,QApplication,QDialog,
QHBoxLayout, QVBoxLayout, QGroupBox, QWidget, QPushButton)
from PyQt5 import QtGui

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
        # okButton = QPushButton("OK")
        # hboxlayout.addWidget(okButton)
        self.groupBox.setLayout(hboxlayout)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("App Title")
        self.setGeometry(500, 200, 800, 800)

        hboxlayout_plt = QHBoxLayout()
        tests = WindowWidgets()
        hboxlayout_plt.addWidget(tests)
        self.setLayout(hboxlayout_plt)

        self.show()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
