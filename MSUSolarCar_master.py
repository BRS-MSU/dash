from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import json

from Common import *
from UIComponents import *


class MSUSolarCarMasterGUI:
    # Create and show the main GUI window
    # Arguments:
    #   style - str - string passed to qt to set the stylesheet
    #   palette - QPalette - palette to use for the color theme
    def create_and_show_gui(self, style, palette, prefs, handle):
        app = QApplication([])
        app.setStyle("Fusion")
        app.setPalette(palette)
        app.setStyleSheet(style)
        right_gui = QWidget()
        right_gui.resize(prefs[0], prefs[1])  # On the RPi it will be 800 * 480
        if prefs[2] == False:
            right_gui.setWindowFlags(right_gui.windowFlags() | Qt.FramelessWindowHint)
            right_gui.move(0, 0)

        right_gui.setWindowTitle("Right GUI - Master")
        main_layout = QHBoxLayout()

        ############################# Right GUI - Master ###############################
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
        ############################ END Right GUI - Master #############################

        main_layout.addWidget(right_gui)
        right_gui.show()
        app.mainWindow = right_gui

        right_turn_signal.set_status("right")

        handle.solar_display = solar_display
        handle.efficiency_display = efficiency_display
        handle.range_display = range_display
        handle.right_turn_signal = right_turn_signal

        return app
    ############################# End of UI code #################################


    def main(self):
        prefs = load_preferences("config.txt")
        print("Dashboard controller for MSU Solar Car 2018-19")
        palette = QPalette();
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 40, 60))
        palette.setColor(QPalette.Background, QColor(20,30,35))
        handle = Handle()
        applet = self.create_and_show_gui("", palette, prefs, handle)
        manager = MasterDataManager(handle)
        manager.update()

        #data_manager = DataManager(handle);
        #data_manager.update_ui();

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


class MasterDataManager(object):
    def __init__(self, handle):
        self.handle = handle
        # TODO pull data from somewhere
        self.power = 2.5
        self.speed = 15
        self.capacity = 88
        self.solar_power = 150
        self.efficiency = 28
        self.range = 35
        self.motor_temp = 42
        self.battery_temp = 31
        self.esc_temp = 33
        self.left_turn_signal_on = 1
        self.right_turn_signal_on = 1

    def update(self):
        # Update UI components
        handle = self.handle
        handle.range_display.update_value(self.range)
        handle.solar_display.update_value(self.solar_power)
        handle.efficiency_display.update_value(self.efficiency)
        if self.right_turn_signal_on == 1:
            handle.right_turn_signal.set_status("right")
        else:
            handle.right_turn_signal.set_status("")

        # Update Slave
        packet = Handle();
        packet.power = self.power
        packet.speed = self.speed
        packet.capacity = self.capacity
        packet.motor_temp = self.motor_temp
        packet.battery_temp = self.battery_temp
        packet.esc_temp = self.esc_temp
        packet.left_turn_signal_on = self.left_turn_signal_on
        print(packet.toJSON())


if __name__ == "__main__":
    app = MSUSolarCarMasterGUI()
    app.main()
