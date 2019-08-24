from PyQt5.QtWidgets import (QMainWindow, QApplication, QDockWidget, QTextEdit, QListWidget)
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import sys

class DockDialog(QMainWindow):
    def __init__(self):
        super().__init__()

        self.InitWindow()

        # self.IPSel = ''
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        self.setWindowTitle("Socket Server")
        self.setGeometry(500, 200, 300, 250)

        self.menu_bar()
        self.show()

    def menu_bar(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        file.addAction("New")
        file.addAction("Save")
        file.addAction("Close")

        self.dock = QDockWidget("Dockable", self)
        self.listwidget = QListWidget()

        list = ["Python", "C++", "Java", "C#"]

        self.listwidget.addItems(list)

        self.dock.setWidget(self.listwidget)

        # Uncomment the lines bellow to make the dockable stick inside the main window with a text input
        # self.setCentralWidget(QTextEdit())
        #
        # self.addDockWidget(Qt.RightDockWidgetArea, self.dock)



App = QApplication(sys.argv)
window = DockDialog()
sys.exit(App.exec())
