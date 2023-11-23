import math

import orekit

import user_interface
import panel_power_calculator

vm = orekit.initVM()

import os.path
import datetime
import orekit.pyhelpers
from org.orekit.time import AbsoluteDate, TimeScalesFactory

from orbit_propagator import OrbitCreator, OrbitPropagator
from angle_calculators import AngleCalculator

if not os.path.isfile('orekit-data.zip'):
    orekit.pyhelpers.download_orekit_data_curdir()

orekit.pyhelpers.setup_orekit_curdir()

# User  input TODO: move this to file reader in io module

#TODO investigate possible offset between UTC and the time we use to calculate J2000 offset in AngleCalculators?
utc = TimeScalesFactory.getUTC()

apogee = 500 * 1000
perigee = 500 * 1000
i = 45.0
omega = 0.0
raan = 0.0
initial_lv = 0.0
initialDate = AbsoluteDate(2023, 3, 21, 12, 0, 0.0, utc)
finalDate = AbsoluteDate(2023, 3, 21, 18, 0, 0.0, utc) # TODO input checks e.g. is initialDate before final date, apogee and perigee etc
timeStep = float(0.05*3600)
panel_area = 1
panel_efficiency = 0.3 #TODO look up typical values

orbit = OrbitCreator(
    apogee,
    perigee,
    i,
    omega,
    raan,
    initial_lv,
    initialDate
).get_orbit()

print(orbit)
state_history = OrbitPropagator(orbit, initialDate, finalDate, timeStep).propagate_orbit()

results = []
for state in state_history:
    angle_calculator = AngleCalculator(state, orbit)
    power_res = panel_power_calculator.calculate_panel_power(panel_area, angle_calculator, panel_efficiency)
    date_string = datetime.datetime.fromisoformat(state.getDate().getComponents(0).toStringRfc3339())
    results.append({
        'date': date_string,
        'power': power_res
    })

user_interface.plot_power_output(results, orbit)
user_interface.write_to_csv(results, orbit)
