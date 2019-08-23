import netifaces
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, \
QGroupBox, QBoxLayout, QListView, QLabel
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.IPselected = ""

        self.setWindowTitle("Choose an IP Address")
        self.setGeometry(500, 200, 600, 250)

        QBtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.clicked.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        group = QGroupBox()
        box = QBoxLayout(QBoxLayout.TopToBottom)
        group.setLayout(box)
        group.setTitle("Adapters list")
        self.layout.addWidget(group)

        view = QListView(self)
        self.model = QStandardItemModel()
        view.clicked.connect(self.treeView_ItemSelected)

        self.list_IP = self.listAddrs()

        view.setModel(self.model)
        box.addWidget(view)

        self.HLayout = QHBoxLayout()

        self.label1 = QLabel(self)
        # self.label1.setFont(QtGui.QFont("Sanserif", 15))
        self.label1.setText("Select an adapter then click Apply")
        self.HLayout.addWidget(self.label1)

        self.layout.addWidget(self.label1)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def treeView_ItemSelected(self, index):
        # print ('selected item index found at %s with data: %s' % (index.row(), str(index.data())))
        # print(self.list_IP[index.row()])
        self.IPselected = self.list_IP[index.row()]

    def listAddrs(self):
        listIP = []
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
                listIP.append(adapt['addr'])
        return listIP
