from PySide2.QtCore import *
from PySide2.QtWidgets import *

import requests

name = 'Name' # Enter your name here!
#chat_url = 'https://build-system.fman.io/chat'
chat_url = '127.0.0.1:65432'

# GUI:
app = QApplication([])
text_area = QTextEdit()
text_area.setFocusPolicy(Qt.NoFocus)
message = QLineEdit()
layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()

app.cou=0
# Event handlers:
def refresh_messages():
    #text_area.setHtml(requests.get(chat_url).text)
    text_area.setHtml("test\n"+str(app.cou))
    app.cou += 1

def send_message():
    requests.post(chat_url, {'name': name, 'message': message.text()})
    message.clear()

# Signals:
message.returnPressed.connect(send_message)
timer = QTimer()
#timer.timeout.connect(refresh_messages)
timer.timeout.connect(refresh_messages)

timer.start(1000)

app.exec_()
