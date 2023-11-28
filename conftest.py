import faulthandler

import pytest
import orekit
vm = orekit.initVM()
import orekit.pyhelpers
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from orbit_propagator import OrbitCreator, OrbitPropagator
from angle_calculators import AngleCalculator
from errors_and_validation import UserInputValidator
orekit.pyhelpers.setup_orekit_curdir()

# Tried to implement a Pytest test suite but encountered a cryptic Python fatal error/segmentation
# fault, possibly related to the interaction between the Java VM  used by Orekit and Pytest. Please
# see test.py for more information.


@pytest.fixture(scope="function")
def set_vm():
    #vm = orekit.initVM()
    yield vm



@pytest.fixture(scope="function")
def set_panel_parameters():
    panel_parameters = {
        'panel_area': 1.0,
        'panel_efficiency': 0.3
    }
    yield panel_parameters


@pytest.fixture(scope="function")
def set_propagation_parameters():
    propagation_parameters = {
        'initial_date': "2023-03-21T12:00:00",
        'final_date': "2023-03-21T18:00:00",
        'timestep': float(0.05 * 3600)
    }
    yield propagation_parameters


@pytest.fixture(scope="function")
def set_orbit_creation_parameters(set_propagation_parameters):
    prop = set_propagation_parameters
    orbit_creation_parameters = {
        'apogee': 500 * 1000,
        'perigee': 500 * 1000,
        'i': 0.0,
        'omega': 0.0,
        'raan': 0.0,
        'initial_lv': 0.0,
        'initial_date': prop['initial_date']
    }
    yield orbit_creation_parameters

@pytest.fixture(scope="function")
def set_input_parameter_dictionary(set_panel_parameters, set_propagation_parameters, set_orbit_creation_parameters):
    parameter_dictionary = {
        'panel_parameters': set_panel_parameters,
        'orbit_creation_parameters': set_orbit_creation_parameters,
        'propagation_parameters': set_propagation_parameters
    }
    yield parameter_dictionary


@pytest.fixture(scope="function")
def get_sample_orbit(set_input_parameter_dictionary):
    validator = UserInputValidator(set_input_parameter_dictionary)
    orbit_creation_parameters, _, _ = validator.validate_input()
    orbit = OrbitCreator(orbit_creation_parameters).get_orbit()
    yield orbit


@pytest.fixture(scope="function")
def get_sample_propagation(get_sample_orbit, set_input_parameter_dictionary):
    validator = UserInputValidator(set_input_parameter_dictionary)
    _, propagation_parameters, _ = validator.validate_input()
    orbit_propagator = OrbitPropagator(get_sample_orbit, propagation_parameters)
    yield orbit_propagator.propagate_orbit()


@pytest.fixture(scope="function")
def get_sample_angle_calculator(get_sample_propagation, get_sample_orbit):
    yield AngleCalculator(get_sample_propagation[0], get_sample_orbit)

