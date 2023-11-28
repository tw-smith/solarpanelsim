import faulthandler

import pytest
import math
from angle_calculators import AngleCalculator
from errors_and_validation import UserInputValidator, UserInputError

# Tried to implement tests but encountered an error where Python would encounter a
# fatal  error/segmentation fault and Pytest would crash. Suspect it is something to
# do with the Java VM which Orekit uses as the error trace also had a bunch of Java
# errors. Also, the error always seemed to occur on the first use of Orekit "AbsoluteDate".
# Spent a bit of time trying to work out the source of the error but eventually decided
# improving other areas of the program would be a better use of my time. If I did
# have time to resolve the error and write a test suite, here is what I would look to cover:
# - Does the user input validator catch all the conceivable errors that a user could make?
# - Do the angle calculators give the expected results? e.g. check there aren't any sin/cos or +/- mistakes
# - Does the output manager give the expected file names even with odd orbit parameters?
# - Does the output manager create the required directories when they don't exist?
# - Does the solar panel power calculator calculate the correct values, including setting to zero when effective area is "negative"?

# After some research, disabling the Pytest fault handler with the command below stops the segfault halting tests, but I
# would still like to find out exactly what is going on before blindly relying on this approach.

# https://stackoverflow.com/questions/57523762/pytest-windows-fatal-exception-code-0x8001010d
# https://gitlab.orekit.org/orekit-labs/python-wrapper/-/issues/430
faulthandler.disable()


def test_user_input_validation_missing_panel_params(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary.pop('panel_parameters')
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_missing_orbit_params(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary.pop('orbit_creation_parameters')
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_missing_propagation_params(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary.pop('propagation_parameters')
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_missing_apogee(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['orbit_creation_parameters'].pop('apogee')
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_missing_final_date(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['propagation_parameters'].pop('final_date')
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_missing_panel_area(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['panel_parameters'].pop('panel_area')
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_date_mismatch(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['propagation_parameters']['final_date'] = "2023-03-20T12:00:00"
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_negative_timestep(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['propagation_parameters']['timestep'] = -0.5
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_negative_apogee(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['orbit_creation_parameters']['apogee'] = -4000
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_negative_perigee(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['orbit_creation_parameters']['perigee'] = -4000
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_apogee_perigee_mismatch(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['orbit_creation_parameters']['apogee'] = input_parameter_dictionary['orbit_creation_parameters']['perigee'] - 5
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_negative_panel_area(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['panel_parameters']['panel_area'] = -1
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_user_input_validation_negative_panel_efficiency(set_input_parameter_dictionary):
    input_parameter_dictionary = set_input_parameter_dictionary
    input_parameter_dictionary['panel_parameters']['panel_efficiency'] = -1
    validator = UserInputValidator(input_parameter_dictionary)
    with pytest.raises(UserInputError):
        validator.validate_input()


def test_angle_calculators(get_sample_orbit, get_sample_propagation):
    # Test sun longitude
    angle_calculator = AngleCalculator(get_sample_propagation[0],  get_sample_orbit)
    # Longitude at midday on 22/11/23 from https://clearskytonight.com/projects/astronomycalculator/sun/sunlongitude.html
    assert round(math.degrees(angle_calculator.get_sun_longitude()), 1) == 239.9

    # Test satellite longitude
    raan = get_sample_orbit.getRightAscensionOfAscendingNode()
    true_anomaly = get_sample_orbit.getTrueAnomaly()
    sun_longitude = angle_calculator.get_sun_longitude()
    assert angle_calculator.get_satellite_true_longitude() == raan + true_anomaly + sun_longitude

    # Test beta angle (assert value from careful hand calculation)
    assert round(angle_calculator.get_beta_angle(), 3) == -0.352
