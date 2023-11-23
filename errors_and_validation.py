import datetime


class UserInputError(Exception):
    def __init__(self, error_message):
        super().__init__()
        self.error_message = error_message

    def __str__(self):
        return self.error_message


class UserInputValidator:
    def __init__(self, parameter_dict):
        self.parameter_dict = parameter_dict
        self.required_orbit_parameters = ['apogee', 'perigee', 'i', 'omega', 'raan', 'initial_lv']
        self.required_propagation_parameters = ['initial_date', 'final_date', 'timestep']
        self.required_panel_parameters = ['panel_area', 'panel_efficiency']

    def validate_input(self):
        if ('propagation_parameters' not in self.parameter_dict or
                'orbit_creation_parameters' not in self.parameter_dict or
                'panel_parameters' not in self.parameter_dict):
            raise UserInputError("propagation, orbit_creation or panel parameters missing from input")

        propagation_parameters = self.parameter_dict['propagation_parameters']
        orbit_creation_parameters = self.parameter_dict['orbit_creation_parameters']
        panel_parameters = self.parameter_dict['panel_parameters']

        for parameter in self.required_orbit_parameters:
            if parameter not in orbit_creation_parameters:
                raise UserInputError(f"Parameter {parameter} is missing from orbit parameters!")
        for parameter in self.required_propagation_parameters:
            if parameter not in propagation_parameters:
                raise UserInputError(f"Parameter {parameter} is missing from propagation parameters!")
        for parameter in self.required_panel_parameters:
            if parameter not in panel_parameters:
                raise UserInputError(f"Parameter {parameter} is missing from panel parameters!")

        # We need to convert the ISO8601 strings to Python datetimes to do before/after validation check
        initial_date_datetime = datetime.datetime.fromisoformat(propagation_parameters['initial_date'])
        final_date_datetime = datetime.datetime.fromisoformat(propagation_parameters['final_date'])

        if final_date_datetime < initial_date_datetime:
            raise UserInputError("Final date must be after initial date!")

        # If dates are OK, replace the IS8601 strings with the datetime objects because we will
        # need datetime objects to do the conversion to Orekit AbsoluteDate in the next step back
        # in InputManager.get_parameter_inputs()
        propagation_parameters['initial_date'] = initial_date_datetime
        propagation_parameters['final_date'] = final_date_datetime

        if propagation_parameters['timestep'] <= 0:
            raise UserInputError("The timestep must be positive!")

        if (orbit_creation_parameters['apogee'] <= 0 or
                orbit_creation_parameters['perigee'] <= 0 or
                orbit_creation_parameters['apogee'] < orbit_creation_parameters['perigee']
        ):
            raise UserInputError("Error with perigee or apogee! Must be positive and ap > pe")

        if panel_parameters['panel_area'] <= 0:
            raise UserInputError("Panel area must be positive.")

        if panel_parameters['panel_efficiency'] <= 0:
            raise UserInputError("Panel efficiency must be positive")

        return orbit_creation_parameters, propagation_parameters, panel_parameters
