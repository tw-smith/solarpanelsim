import datetime
import os.path
import orekit

vm = orekit.initVM() #TODO move this further down if we can

import orekit.pyhelpers
from org.orekit.time import AbsoluteDate, TimeScalesFactory

from orbit_propagator import OrbitCreator, OrbitPropagator
from angle_calculators import AngleCalculator
import panel_power_calculator
from user_interface import OutputManager

if not os.path.isfile('orekit-data.zip'):
    orekit.pyhelpers.download_orekit_data_curdir()

orekit.pyhelpers.setup_orekit_curdir()

# User  input TODO: move this to file reader in io module

#TODO investigate possible offset between UTC and the time we use to calculate J2000 offset in AngleCalculators?
utc = TimeScalesFactory.getUTC()

propagation_parameters = {
    'initial_date': AbsoluteDate(2023, 3, 21, 12, 0, 0.0, utc),
    'final_date': AbsoluteDate(2023, 3, 21, 18, 0, 0.0, utc),
    'timestep': float(0.05*3600)
}

orbit_creation_parameters = {
    'apogee': 500*1000,
    'perigee': 500*1000,
    'i': 70.0,
    'omega': 0.0,
    'raan': 45.0,
    'initial_lv': 0.0,
    'initial_date': propagation_parameters['initial_date']
}

panel_parameters = {
    'panel_area': 1.0,
    'panel_efficiency': 0.3
}

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
output_manager.plot_power_output()
output_manager.write_to_csv()
