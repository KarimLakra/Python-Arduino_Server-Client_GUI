from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton
import pyqtgraph as pg
from XAxisTime import TimeAxisItem, timestamp
import sys, time
import numpy as np

class ExampleWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.btn = False
        self.timer = pg.QtCore.QTimer()

        self.plot = pg.PlotWidget(
            title="Example plot",
            labels={'left': 'Reading / mV'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )
        self.initWin()
        self.show()

    def initWin(self):
        self.plot.setYRange(-5, 5)
        self.plot.setXRange(timestamp(), timestamp() + 100)
        self.plot.showGrid(x=True, y=True)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.plot, 0, 0)

        self.plotCurve = self.plot.plot(pen='y')

        self.plotData = {'x': [], 'y': []}

        self.GetDataBtn = QPushButton("Connect")
        self.GetDataBtn.clicked.connect(self.ticker)
        self.GetDataBtn.setMinimumHeight(50)
        self.GetDataBtn.setMinimumWidth(180)
        self.layout.addWidget(self.GetDataBtn, 1, 0)

    def updatePlot(self):
        a = np.random.rand()
        self.plotData['y'].append(a)
        self.plotData['x'].append(timestamp())

        self.plotCurve.setData(self.plotData['x'], self.plotData['y'])

    def ticker(self):
        if self.btn == False:

            self.timer.timeout.connect(self.updatePlot)
            self.timer.start(500)
            self.btn = True
            self.GetDataBtn.setStyleSheet("background-color: green")
            self.GetDataBtn.setText("Disconnect")
        else:
            self.timer.stop()
            self.btn = False
            self.GetDataBtn.setStyleSheet("background-color: red")
            self.GetDataBtn.setText("Connect")

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = ExampleWidget()
    sys.exit(App.exec())
