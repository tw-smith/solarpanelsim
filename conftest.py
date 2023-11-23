import pytest
import orekit
vm = orekit.initVM()
import orekit.pyhelpers
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from orbit_propagator import OrbitCreator, OrbitPropagator
from angle_calculators import AngleCalculator
orekit.pyhelpers.setup_orekit_curdir()

# Tried to implement a Pytest test suite but encountered a cryptic Python fatal error/segmentation
# fault, possibly related to the interaction between the Java VM  used by Orekit and Pytest. Please
# see test.py for more information.


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
        'initial_date': AbsoluteDate(2023, 11, 22, 12, 0, 0.0, TimeScalesFactory.getUTC()),
        'final_date': AbsoluteDate(2023, 11, 22, 18, 0, 0.0, TimeScalesFactory.getUTC()),
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
def get_sample_orbit(set_orbit_creation_parameters):
    orbit = OrbitCreator(set_orbit_creation_parameters).get_orbit()
    yield orbit


@pytest.fixture(scope="function")
def get_sample_propagation(get_sample_orbit, set_propagation_parameters):
    orbit_propagator = OrbitPropagator(get_sample_orbit, set_propagation_parameters)
    yield orbit_propagator.propagate_orbit()


@pytest.fixture(scope="function")
def get_sample_angle_calculator(get_sample_propagation, get_sample_orbit):
    yield AngleCalculator(get_sample_propagation[0], get_sample_orbit)

