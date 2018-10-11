from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


############################# Beginning of GUI code #################################

# Create and show the main GUI window
# Arguments:
#   style - str - string passed to qt to set the stylesheet
#   palette - QPalette - palette to use for the color theme
def create_and_show_gui(style, palette):
    app = QApplication([])
    app.setStyle("Fusion")
    app.setPalette(palette)
    app.setStyleSheet(style)
    window = QWidget()
    window.resize(1300, 400)  # On the RPi it will be 1600 * 480
    # window.setWindowFlags(window.windowFlags() | Qt.FramelessWindowHint)
    window.setWindowTitle("Display 1 of 2 | Display 2 of 2")
    main_layout = QHBoxLayout()

    ############################## Left GUI ###############################
    left_gui = QWidget();
    # top-level window layout
    left_main_layout = QVBoxLayout()
    # Layout for the top low
    left_top_row_layout = QHBoxLayout()
    left_top_row = QWidget();

    power_display = DashDisplay("POWER - Kilowatts", 0, 0.9);
    speed_display = DashDisplay("SPEED - MPH", 0)
    capacity_display = DashDisplay("CAPACITY - Percent", 100, 0.9);

    left_top_row_layout.addWidget(power_display)
    left_top_row_layout.addWidget(speed_display)
    left_top_row_layout.addWidget(capacity_display)

    left_top_row.setLayout(left_top_row_layout)
    left_main_layout.addWidget(left_top_row)

    # Layout for the bottom row
    left_bottom_row_layout = QGridLayout()
    left_bottom_row = QWidget()
    left_turn_signal = TurnSignal()
    left_bottom_row_layout.addWidget(QWidget(), 1, 2)
    left_bottom_row_layout.addWidget(left_turn_signal, 2, 1);

    left_bottom_row.setLayout(left_bottom_row_layout)

    left_main_layout.addWidget(left_bottom_row)
    left_gui.setLayout(left_main_layout)
    ############################ END Left GUI #############################
    ############################# Right GUI ###############################
    right_gui = QWidget()
    # top-level window layout
    right_main_layout = QVBoxLayout()
    # Layout for the top low
    right_top_row_layout = QHBoxLayout()
    right_top_row = QWidget()

    solarDisplay = DashDisplay("Solar Power - Watts", 5000, 0.7)
    efficiencyDisplay = DashDisplay("Watt Hrs per Mile", 50)
    rangeDisplay = DashDisplay("RANGE left - Miles", 150, 0.8)

    right_top_row_layout.addWidget(solarDisplay)
    right_top_row_layout.addWidget(efficiencyDisplay)
    right_top_row_layout.addWidget(rangeDisplay)

    right_top_row.setLayout(right_top_row_layout)
    right_main_layout.addWidget(right_top_row)

    # Layout for the bottom row
    right_bottom_row_layout = QGridLayout()
    right_bottom_row = QWidget()
    right_turn_signal = TurnSignal()
    right_bottom_row_layout.addWidget(QWidget(), 1, 1)
    right_bottom_row_layout.addWidget(right_turn_signal, 4, 4);

    right_gui.setLayout(right_main_layout)
    right_bottom_row.setLayout(right_bottom_row_layout)
    right_main_layout.addWidget(right_bottom_row)
    ############################ END Right GUI #############################

    main_layout.addWidget(left_gui)
    main_layout.addWidget(right_gui)
    window.setLayout(main_layout)
    window.show()
    app.mainWindow = window

    left_turn_signal.set_status("left")
    right_turn_signal.set_status("right")

    return app


class DashDisplay(QWidget):
    def __init__(self, title, content, scale=1):
        super(DashDisplay, self).__init__()
        self.initUI(title, content, scale)

    def initUI(self, title, content, scale):
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


class TurnSignal(QWidget):

    def __init__(self):
        super(TurnSignal, self).__init__()
        self.status = "off"

    def set_status(self, st):
        if (self.status != st):
            self.status = st
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        width = self.width()
        height = self.height()

        centerColor = Qt.yellow;
        leftColor = Qt.yellow;
        rightColor = Qt.yellow;

        if (self.status != "left" and self.status != "right"):
            centerColor = Qt.black;
        if (self.status != "left"):
            leftColor = Qt.black
        if (self.status != "right"):
            rightColor = Qt.black

        qp.fillRect(0, 0, width, height, Qt.black)
        qp.fillRect(width * 0.15, height * 0.35, width * 0.7 + 1, height * 0.3, centerColor)
        left_path = QPainterPath()
        left_path.moveTo(width * 0.15, 0)
        left_path.lineTo(width * 0.15, height)
        left_path.lineTo(0, height / 2)
        right_path = QPainterPath()
        right_path.moveTo(width * 0.85, 0)
        right_path.lineTo(width * 0.85, height)
        right_path.lineTo(width, height / 2)
        qp.fillPath(left_path, leftColor)
        qp.fillPath(right_path, rightColor)
        qp.end()

def message_box(str = "untitled"):
    alert = QMessageBox()
    alert.setModal(True)
    alert.setText(str)
    alert.exec_()
############################# End of UI code #################################


def load_strings(path):
    fileref = open(path, "r")
    rtn = fileref.readlines()
    fileref.close()
    return rtn


def load_preferences(path):
    text = load_strings(path)
    for line in text:

        width = 800
        height = 400
        decorated = True

        value = line.split("=")
        key = value[0]
        value = value[1].rstrip()

        if key == "width":
            width = int(value)
        if key == "height":
            height = int(value)
        if key == "decorated":
            value = "false"
            if value.lower == "false":
                decorated = False
            else:
                decorated = True
    return (width, height, decorated)


def main():
    #print(load_preferences("config.txt"))
    #return
    print("Dashboard controller for MSU Solar Car 2018-19")
    palette = QPalette();
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Button, QColor(0, 40, 60))
    palette.setColor(QPalette.Background, Qt.darkGray)
    applet = create_and_show_gui("", palette)
    applet.exec_()


main()
