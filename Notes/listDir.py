import sys
import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QBoxLayout, QDialogButtonBox, QListView

class asset(QDialog):

    def __init__(self,parent=None):
        super(asset, self).__init__(parent)
        self.assetList = QListView(self)
        self.assetList.clicked.connect(self.on_treeView_clicked)

        ######################################################################
        # ----------------- ADD ITEMS----------------------------------------
        ######################################################################

        list_data = listDirs('D:\\')
        dir = listModel(list_data)
        self.assetList.setModel(dir)

        self.setStyleSheet('''

                            *{
                            background-color : rgb(65,65,65);
                            color : rgb(210,210,210);
                            alternate-background-color:rgb(55,55,55);
                            }

                            QTreeView,QListView,QLineEdit{
                            background-color : rgb(50,50,50);
                            color : rgb(210,210,210);
                            }

                            '''
                           )
        self.setFocus()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        print ('selected item index found at %s with data: %s' % (index.row(), str(index.data())))

class listModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()

def listDirs(*path):
    completePath = os.path.join(*path)
    dirs = os.listdir(os.path.abspath(completePath))
    outputDir = []
    for dir in dirs:
        if os.path.isdir(os.path.join(completePath,dir)):
            outputDir.append(dir)
    return outputDir



if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle('plastique')
    main = asset()
    main.resize(200,200)
    main.show()
    sys.exit(app.exec_())
