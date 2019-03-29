from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import json

from Common import *
from UIComponents import *


class MSUSolarCarSlaveGUI():
    # Create and show the main GUI window
    # Arguments:
    #   style - str - string passed to qt to set the stylesheet
    #   palette - QPalette - palette to use for the color theme
    def create_and_show_gui(main, style, palette, prefs, handle):
        app = QApplication([])
        app.setStyle("Fusion")
        app.setPalette(palette)
        app.setStyleSheet(style)

        left_gui = QWidget();
        left_gui.resize(prefs[0], prefs[1])  # On the RPi it will be 800 * 480
        if prefs[2] == False:
            left_gui.setWindowFlags(left_gui.windowFlags() | Qt.FramelessWindowHint)
            left_gui.move(0, 0)

        left_gui.setWindowTitle("Left GUI - Slave");

        ############################## Left GUI ###############################
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

        motor_temp_display = DashDisplay("Motor temp °C", "...", 0.4)
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

        left_gui.show()
        app.mainWindow = left_gui

        left_turn_signal.set_status("left")

        handle.power_display = power_display
        handle.speed_display = speed_display
        handle.capacity_display = capacity_display
        handle.motor_temp_display = motor_temp_display
        handle.esc_temp_display = esc_temp_display
        handle.batt_temp_display = batt_temp_display
        handle.left_turn_signal = left_turn_signal

        return app


    ############################# End of UI code #################################

    def main(self):
        prefs = load_preferences("config.txt")
        print("Dashboard controller for MSU Solar Car 2018-19")
        palette = QPalette();
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 40, 60))
        palette.setColor(QPalette.Background, QColor(20, 30, 35))

        handle = Handle()
        applet = self.create_and_show_gui("", palette, prefs, handle)

        data_manager = SlaveDataManager(handle);
        data_manager.update_ui('{ "battery_temp": 31, "capacity": 88, "esc_temp": 33, "left_turn_signal_'
                               'on": 1, "motor_temp": 42, "power": 2.5, "speed": 15 }')

        applet.exec_()


class SlaveDataManager(object):
    def __init__(self, handle):
        self.handle = handle

    def update_ui(self, message):
        data = json.loads(message)
        handle = self.handle
        handle.power_display.update_value(data["power"])
        handle.speed_display.update_value(data["speed"])
        handle.capacity_display.update_value(data["capacity"])
        handle.batt_temp_display.update_value(data["battery_temp"])
        handle.motor_temp_display.update_value(data["motor_temp"])
        handle.esc_temp_display.update_value(data["esc_temp"])
        if data["left_turn_signal_on"] == 1:
            handle.left_turn_signal.set_status("left")
        else:
            handle.left_turn_signal.set_status("")



if __name__ == "__main__":
    app = MSUSolarCarSlaveGUI()
    app.main()
