import math


def calculate_panel_power(panel_parameters, angle_calculator):
    # Watts per metre square from sun at 1AU.
    # Value from https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010GL045777
    SOLAR_CONSTANT = 1361
    area_modifier = (math.cos(angle_calculator.get_satellite_true_longitude()) *
                      math.cos(angle_calculator.get_beta_angle()))
    effective_area = panel_parameters['panel_area'] * area_modifier
    if effective_area <= 0:
        return 0
    else:
        return SOLAR_CONSTANT * panel_parameters['panel_efficiency'] * effective_area
