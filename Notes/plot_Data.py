import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from PyQt5.QtCore import QTimer
import random

# plt.style.use('plotStyle')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
# timerRND = QTimer()
# timerRND.timeout.connect(randomNum)
# timerRND.start(1000)
xs = []
ys = []
count = 0
def randomNum(i):
    global count
    lines = random.randint(1,101)

    # for line in lines:
        # if len(line) > 1:
        # x, y = line.split(',')
    xs.append(count)
    ys.append(lines)
    # print(xs, ys)
    ax1.clear()
    ax1.plot(xs,ys)
    count += 1

ani = animation.FuncAnimation(fig, randomNum, interval=1000)
plt.show()
