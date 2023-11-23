import math


def calculate_panel_power(panel_area, angle_calculator, panel_efficiency):
    SOLAR_CONSTANT = 1366
    area_modifier = (math.cos(angle_calculator.get_satellite_true_longitude()) *
                      math.cos(angle_calculator.get_sun_longitude()))
    effective_area = panel_area * area_modifier
    if effective_area <= 0:
        return 0
    else:
        return SOLAR_CONSTANT * panel_efficiency * effective_area
