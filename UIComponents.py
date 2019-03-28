from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DashDisplay(QWidget):
    def __init__(self, title, content, scale=1.0):
        super(DashDisplay, self).__init__()
        self.init_ui(title, content, scale)

    def init_ui(self, title, content, scale):
        layout = QGridLayout()
        layout.setSpacing(1)
        self.top = QLabel(str(title))
        self.top.setAlignment(Qt.AlignCenter)
        self.bottom = QLabel(str(content))
        font = self.bottom.font()
        font.setPointSize(72 * scale)
        self.bottom.setFont(font)
        self.bottom.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.top, 1, 1)
        layout.addWidget(self.bottom, 2, 1, 5, 1)
        self.setLayout(layout)
        self.setStyleSheet("QLabel {background: palette(button)}")

    def update_value(self, value):
        self.bottom.setText(str(value))

    def update_name(self, name):
        self.top.setText(str(name))


class StatusLabel(QLabel):
    def __init__(self, text, scale):
        super(StatusLabel, self).__init__()
        self.init_ui(text, scale)
        self.status = True;

    def init_ui(self, text, scale):
        self.setText(text)
        font = self.font()
        font.setPointSize(72 * scale)
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)
        self.set_status(False)

    def set_status(self, st):
        self.status = st
        if st == "true":
            self.setStyleSheet("background-color: #0C4")
        elif st == "false":
            self.setStyleSheet("background-color: #F31")
        else:
            self.setStyleSheet("background-color: #981")



class TurnSignal(QWidget):

    def __init__(self):
        super(TurnSignal, self).__init__()
        self.status = "off"
        self.fg = QColor(0,255,92);
        self.bg = QColor(0,0,0,0);

    def set_status(self, st):
        if (self.status != st):
            self.status = st
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        width = self.width()
        height = self.height()

        center_color = self.fg;
        left_color = self.fg;
        right_color = self.fg;

        if (self.status != "left" and self.status != "right"):
            center_color = self.bg;
        if (self.status != "left"):
            left_color = self.bg;
        if (self.status != "right"):
            right_color = self.bg;

        qp.fillRect(0, 0, width, height, self.bg)
        qp.fillRect(width * 0.15, height * 0.35, width * 0.7 + 1, height * 0.3, center_color)
        left_path = QPainterPath()
        left_path.moveTo(width * 0.15, 0)
        left_path.lineTo(width * 0.15, height)
        left_path.lineTo(0, height / 2)
        right_path = QPainterPath()
        right_path.moveTo(width * 0.85, 0)
        right_path.lineTo(width * 0.85, height)
        right_path.lineTo(width, height / 2)
        qp.fillPath(left_path, left_color)
        qp.fillPath(right_path, right_color)
        qp.end()

def message_box(str = "untitled"):
    alert = QMessageBox()
    alert.setModal(True)
    alert.setText(str)
    alert.exec_()