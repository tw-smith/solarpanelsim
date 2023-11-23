import datetime
import os.path
import sys
import orekit
vm = orekit.initVM() #TODO move this further down if we can
import orekit.pyhelpers
from orbit_propagator import OrbitCreator, OrbitPropagator
from angle_calculators import AngleCalculator
from user_interface import OutputManager, InputManager
import panel_power_calculator


def solarsimulator(input_params=None):
    if not os.path.isfile('orekit-data.zip'):
        orekit.pyhelpers.download_orekit_data_curdir()
    orekit.pyhelpers.setup_orekit_curdir()
    if not input_params:
        input_params = sys.argv[1]
    input_manager = InputManager(input_params)
    orbit_creation_parameters, propagation_parameters, panel_parameters = input_manager.get_parameter_inputs()

    orbit = OrbitCreator(orbit_creation_parameters).get_orbit()
    state_history = OrbitPropagator(orbit, propagation_parameters).propagate_orbit()

    results = []
    for state in state_history:
        angle_calculator = AngleCalculator(state, orbit)
        power_res = panel_power_calculator.calculate_panel_power(panel_parameters, angle_calculator)
        date_string = datetime.datetime.fromisoformat(state.getDate().getComponents(0).toStringRfc3339())
        results.append({
            'date': date_string,
            'power': power_res
        })

    output_manager = OutputManager(results, orbit)
    output_manager.write_to_csv()
    output_manager.plot_power_output()



if __name__ == '__main__':
    solarsimulator()
