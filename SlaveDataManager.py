class SlaveDataManager(object):
    def __init__(self, handle):
        self.handle = handle
        # TODO accept commands from master
        self.power = 2.5
        self.speed = 15
        self.capacity = 88
        self.solar_power = 150
        self.efficiency = 28
        self.range = 35
        self.motor_temp = 42
        self.battery_temp = 31
        self.esc_temp = 33

    def update_ui(self):
        handle = self.handle
        handle.power_display.update_value(self.power)
        handle.speed_display.update_value(self.speed)
        handle.capacity_display.update_value(self.capacity)
        handle.solar_poewr_displaty.update_value(self.solar_power)
        handle.solar_poewr_displaty.update_value(self.efficiency)
        handle.range_display.update_value(self.range)
        handle.batt_temp_display.update_value(self.battery_temp)
        handle.motor_temp_display.update_value(self.motor_temp)
        handle.esc_temp_display.update_value(self.esc_temp)