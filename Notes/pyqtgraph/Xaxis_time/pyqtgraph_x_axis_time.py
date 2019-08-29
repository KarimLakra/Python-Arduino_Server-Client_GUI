from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
import pyqtgraph as pg
from utils import TimeAxisItem, timestamp
import sys

class ExampleWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.plot = pg.PlotWidget(
            title="Example plot",
            labels={'left': 'Reading / mV'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )
        self.plot.setYRange(0, 5000)
        self.plot.setXRange(timestamp(), timestamp() + 100)
        self.plot.showGrid(x=True, y=True)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.plot, 0, 0)

        self.plotCurve = self.plot.plot(pen='y')

        self.plotData = {'x': [], 'y': []}
        self.show()
    def updatePlot(self, newValue):
        self.plotData['y'].append(newValue)
        self.plotData['x'].append(timestamp())

        self.plotCurve.setData(self.plotData['x'], self.plotData['y'])

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = ExampleWidget()
    sys.exit(App.exec())
