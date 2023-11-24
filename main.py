import datetime
import os.path
import sys
import orekit
vm = orekit.initVM()
import orekit.pyhelpers
from orbit_propagator import OrbitCreator, OrbitPropagator
from angle_calculators import AngleCalculator
from user_interface import OutputManager, InputManager
import panel_power_calculator


def solarsimulator(input_params=None):

    # Download the orekit data pack if we don't already have it and set it up for use in the Python wrapper
    if not os.path.isfile('orekit-data.zip'):
        orekit.pyhelpers.download_orekit_data_curdir()
    orekit.pyhelpers.setup_orekit_curdir()

    # Get input parameters either from input.json or input dictionary and pass them to the InputManager for validation
    # and conversion.
    if not input_params:
        input_params = sys.argv[1]
    input_manager = InputManager(input_params)
    orbit_creation_parameters, propagation_parameters, panel_parameters = input_manager.get_parameter_inputs()

    # With our validated inputs, create a Keplerian orbit in Orekit, propagate that orbit and get the history of
    # SpacecraftState objects.
    orbit = OrbitCreator(orbit_creation_parameters).get_orbit()
    state_history = OrbitPropagator(orbit, propagation_parameters).propagate_orbit()

    # For each item in our history of SpacecraftState objects, create an AngleCalculator object which provides us with
    # all the various angles needed to work out our effective panel area. Get our calculated solar panel power and add
    # it to a list of results along with the time data.
    results = []
    for state in state_history:
        angle_calculator = AngleCalculator(state, orbit)
        power_res = panel_power_calculator.calculate_panel_power(panel_parameters, angle_calculator)
        state_rfc3339_date = state.getDate().getComponents(0).toStringRfc3339()
        # We need to strip the Z from the end of the RFC3339 string to stay compatible with Python versions before 3.11
        # https://docs.python.org/3/library/datetime.html#datetime.time.fromisoformat
        python_friendly_date = state_rfc3339_date.replace('Z', '')
        date_string = datetime.datetime.fromisoformat(python_friendly_date)
        results.append({
            'date': date_string,
            'power': power_res
        })

    # Pass results list to OutputManager for plotting and csv generation
    output_manager = OutputManager(results, orbit)
    output_manager.write_to_csv()
    output_manager.plot_power_output()
    return results


if __name__ == '__main__':
    solarsimulator()
