import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np

app = QApplication(sys.argv)

x = np.arange(1000)
y = np.random.normal(size=(3,1000))

plotWidget = pg.plot(title="Three Plot curves")

for i in range(3):
    plotWidget.plot(x, y[i], pen=(i,3))

status = app.exec_()
sys.exit(status)
