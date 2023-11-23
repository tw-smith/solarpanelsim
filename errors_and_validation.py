from org.orekit.time import AbsoluteDate

class UserInputError(Exception):
    def __init__(self, error_message):
        super().__init__()
        self.error_message = error_message

    def __str__(self):
        return self.error_message


class UserInputValidator:
    def __init__(self, propagation_parameters, orbit_creation_parameters, panel_parameters):
        self.propagation_parameters = propagation_parameters
        self.orbit_creation_parameters = orbit_creation_parameters
        self.panel_parameters = panel_parameters

    def validate_input(self):
        if not self.propagation_parameters['final_date'].isAfter(self.propagation_parameters['initial_date']):
            raise UserInputError("Final date must be after initial date!")

        if self.propagation_parameters['timestep'] <= 0:
            raise UserInputError("The timestep must be positive!")

        if (self.orbit_creation_parameters['apogee'] <= 0 or
            self.orbit_creation_parameters['perigee'] <= 0 or
            self.orbit_creation_parameters['apogee'] < self.orbit_creation_parameters['perigee']
        ):
            raise UserInputError("Error with perigee or apogee! Must be positive and ap > pe")

        if self.panel_parameters['panel_area'] <= 0:
            raise UserInputError("Panel area must be positive.")

        if self.panel_parameters['panel_efficiency'] <= 0:
            raise UserInputError("Panel efficiency must be positive")


