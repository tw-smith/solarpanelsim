import orekit
vm = orekit.initVM()

import os.path
import orekit.pyhelpers
from org.orekit.time import AbsoluteDate, TimeScalesFactory

from orbit_propagator import OrbitCreator, OrbitPropagator

if not os.path.isfile('/orekit-data.zip'):
    orekit.pyhelpers.download_orekit_data_curdir()

orekit.pyhelpers.setup_orekit_curdir()

# User  input TODO: move this to file reader in io module

utc = TimeScalesFactory.getUTC()

apogee = 500 * 1000
perigee = 500 * 1000
i = 0.0
omega = 0.0
raan = 0.0
initial_lv = 0.0
initialDate = AbsoluteDate(2023, 3, 21, 12, 0, 0.0, utc)
finalDate = AbsoluteDate(2023, 4, 1, 12, 0, 0.0, utc) # TODO input checks e.g. is initialDate before final date, apogee and perigee etc
timeStep = float(0.05*3600)

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

print(OrbitPropagator(orbit, initialDate, finalDate, timeStep).propagate_orbit())
