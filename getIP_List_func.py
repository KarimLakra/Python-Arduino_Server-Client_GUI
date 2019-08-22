# https://github.com/qingfengxia/Cfd/blob/master/FoamCaseBuilder/ChoiceDialog.py

# https://stackoverflow.com/questions/30080927/pop-up-dialog-from-one-button-on-the-main-window-pyqt5
# from PyQt5.QtWidgets import QMainWindow, QApplication, QGroupBox, QPushButton, QHBoxLayout, QVBoxLayout, QBoxLayout, QListView, QDialog
from PyQt5.QtWidgets import  QBoxLayout, QGroupBox, QListView, QVBoxLayout, QDialog, QDialogButtonBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtCore, QtGui, QtWidgets
import netifaces

# class SerachAdapter(QtWidgets.QWidget):
class SerachAdapter(QDialog):
    def setupDialog(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowIcon(QtGui.QIcon("network-port-icon.png"))
        Dialog.resize(500, 200)
        self.VL = QtWidgets.QVBoxLayout(Dialog)
        self.VL.setObjectName("VL")

        self.HL0 = QtWidgets.QHBoxLayout()
        self.HL0.setObjectName("HL0")

        group = QGroupBox(Dialog)
        box = QBoxLayout(QBoxLayout.TopToBottom)
        group.setLayout(box)
        group.setTitle("Adapters list")
        self.HL0.addWidget(group)

        view = QListView(Dialog)
        self.model = QStandardItemModel()
        self.listAddrs()

        view.setModel(self.model)
        box.addWidget(view)

        self.VL.addLayout(self.HL0)

        self.HL1 = QtWidgets.QHBoxLayout()
        self.HL1.setObjectName("HL1")

        self.VL.addLayout(self.HL1)

        self.HL2 = QtWidgets.QHBoxLayout()
        self.HL2.setObjectName("HL2")

        self.SelectButton = QtWidgets.QPushButton(Dialog)
        self.SelectButton.setObjectName("SelectButton")
        self.HL2.addWidget(self.SelectButton)

        self.CancelButton = QtWidgets.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.HL2.addWidget(self.CancelButton)
        self.VL.addLayout(self.HL2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # connect the two functions
        self.SelectButton.clicked.connect(self.accept)
        self.CancelButton.clicked.connect(self.reject())


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select Ip address"))
        self.SelectButton.setText(_translate("Dialog", "Select"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))

    # 2 sample functions
    def accept(self):
        print("yes")

    def cancel(self):
        self.reject()
        print("exit")


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
