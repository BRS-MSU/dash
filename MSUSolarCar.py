from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from DataManager import *


############################# Beginning of GUI code #################################

# Create and show the main GUI window
# Arguments:
#   style - str - string passed to qt to set the stylesheet
#   palette - QPalette - palette to use for the color theme
def create_and_show_gui(style, palette, prefs, handle):
    app = QApplication([])
    app.setStyle("Fusion")
    app.setPalette(palette)
    app.setStyleSheet(style)
    window = QWidget()
    window.resize(prefs[0], prefs[1])  # On the RPi it will be 1600 * 480
    if prefs[2] == False:
        window.setWindowFlags(window.windowFlags() | Qt.FramelessWindowHint)
        window.move(0, 0)

    window.setWindowTitle("Display 1 of 2 | Display 2 of 2")
    main_layout = QHBoxLayout()

    ############################## Left GUI ###############################
    left_gui = QWidget();
    # top-level window layout
    left_main_layout = QVBoxLayout()
    # Layout for the top low
    left_top_row_layout = QHBoxLayout()
    left_top_row_layout.setContentsMargins(0, 0, 0, 0);
    left_top_row = QWidget();

    power_display = DashDisplay("POWER - Kilowatts", "...", 0.9);
    speed_display = DashDisplay("SPEED - MPH", "...", 1.4)
    capacity_display = DashDisplay("CAPACITY - Percent", "...", 0.9);

    left_top_row_layout.addWidget(power_display)
    left_top_row_layout.addWidget(speed_display)
    left_top_row_layout.addWidget(capacity_display)

    left_top_row.setLayout(left_top_row_layout)
    left_main_layout.addWidget(left_top_row)

    # Layout for the bottom row
    left_bottom_row_layout = QGridLayout()
    left_bottom_row_layout.setContentsMargins(0, 0, 0, 0)
    left_bottom_row = QWidget()
    left_turn_signal = TurnSignal()

    motor_temp_display= DashDisplay("Motor temp °C", "...", 0.4)
    batt_temp_display = DashDisplay("Battery temp °C", "...", 0.4)
    esc_temp_display = DashDisplay("ESC temp °C", "...", 0.4)

    left_bottom_row_layout.addWidget(QWidget(), 1, 2)
    left_bottom_row_layout.addWidget(left_turn_signal, 2, 1)

    left_bottom_row_layout.addWidget(motor_temp_display, 1, 2)
    left_bottom_row_layout.addWidget(batt_temp_display, 2, 2)
    left_bottom_row_layout.addWidget(esc_temp_display, 1, 1)

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
    right_top_row_layout.setContentsMargins(0, 0, 0, 0)
    right_top_row = QWidget()

    range_display = DashDisplay("RANGE left - Miles", "...", 0.8)
    efficiency_display = DashDisplay("Watt Hrs per Mile", "...")
    solar_display = DashDisplay("Solar Power - Watts", "...", 0.7)


    right_top_row_layout.addWidget(range_display)
    right_top_row_layout.addWidget(efficiency_display)
    right_top_row_layout.addWidget(solar_display)

    right_top_row.setLayout(right_top_row_layout)
    right_main_layout.addWidget(right_top_row)

    # Layout for the bottom row
    right_bottom_row_layout = QGridLayout()
    right_bottom_row_layout.setContentsMargins(0, 0, 0, 0)
    right_bottom_row = QWidget()
    right_turn_signal = TurnSignal()

    placeholder1 = StatusLabel("BMS Status", 0.3)
    placeholder2 = StatusLabel("Motor Status", 0.3)
    placeholder3 = StatusLabel("System / Telemetry\n...", 0.3)

    right_bottom_row_layout.addWidget(right_turn_signal, 2, 2)
    right_bottom_row_layout.addWidget(placeholder1, 1, 1)
    right_bottom_row_layout.addWidget(placeholder2, 1, 2)
    right_bottom_row_layout.addWidget(placeholder3, 2, 1)

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

    handle.power_display = power_display
    handle.speed_display = speed_display
    handle.capacity_display = capacity_display
    handle.solar_display = solar_display
    handle.efficiency_display = efficiency_display
    handle.range_display = range_display
    handle.motor_temp_display = motor_temp_display
    handle.esc_temp_display = esc_temp_display
    handle.batt_temp_display = batt_temp_display
    handle.left_turn_signal = left_turn_signal
    handle.right_turn_signal = right_turn_signal

    return app


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
############################# End of UI code #################################


def load_strings(path):
    fileref = open(path, "r")
    rtn = fileref.readlines()
    fileref.close()
    return rtn


def load_preferences(path):
    text = load_strings(path)
    width = 800
    height = 400
    decorated = True
    for line in text:
        value = line.split("=")
        if(len(value) < 2):
            continue
        key = value[0]
        value = value[1].rstrip()

        if key == "width":
            width = int(value)
        if key == "height":
            height = int(value)
        if key == "decorated":
            if value.lower() == "false":
                decorated = False
            else:
                decorated = True

    print("Loaded config. Width="+str(width)+"  Height="+str(height)+"  Decorated="+str(decorated))
    return (width, height, decorated)

class Handle(object):
    pass


def main():
    prefs = load_preferences("config.txt")
    print("Dashboard controller for MSU Solar Car 2018-19")
    palette = QPalette();
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Button, QColor(0, 40, 60))
    palette.setColor(QPalette.Background, QColor(20,30,35))

    handle = Handle()
    applet = create_and_show_gui("", palette, prefs, handle)

    data_manager = DataManager(handle);
    data_manager.update_ui();

    '''
    The following values are references to GUI components
    
    handle.power_display - DashDisplay
    handle.speed_display - DashDisplay
    handle.capacity_display - DashDisplay
    handle.solar_display - DashDisplay
    handle.efficiency_display - DashDisplay
    handle.range_display - DashDisplay
    handle.motor_temp_display - DashDisplay
    handle.esc_temp_display - DashDisplay
    handle.batt_temp_display - DashDisplay
    handle.left_turn_signal - TurnSignal
    handle.right_turn_signal - Turnsignal
    '''

    applet.exec_()

if __name__ == "__main__":
    main()
