import pytest
import math
from angle_calculators import AngleCalculator
from errors_and_validation import UserInputValidator

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


def test_user_input_validation(set_propagation_parameters, set_orbit_creation_parameters, set_panel_parameters):
    propagation_parameters = set_propagation_parameters
    orbit_parameters = set_orbit_creation_parameters
    propagation_parameters['apogee'] = -4000
    validator = UserInputValidator(propagation_parameters, orbit_parameters, set_panel_parameters)
    with pytest.raises(Exception):
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
