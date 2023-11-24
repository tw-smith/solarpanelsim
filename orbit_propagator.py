import math
from org.orekit.orbits import KeplerianOrbit, PositionAngleType
from org.orekit.propagation.analytical import KeplerianPropagator
from org.orekit.utils import Constants
from org.orekit.frames import FramesFactory


class OrbitCreator:
    def __init__(self, orbit_creation_parameters):
        self.apogee = orbit_creation_parameters['apogee']
        self.perigee = orbit_creation_parameters['perigee']
        self.inclination = math.radians(orbit_creation_parameters['i'])
        self.arg_of_periapsis = math.radians(orbit_creation_parameters['omega'])
        self.raan = math.radians(orbit_creation_parameters['raan'])
        self.initial_lv = math.radians(orbit_creation_parameters['initial_lv'])
        self.initial_date = orbit_creation_parameters['initial_date']
        self.inertial_frame = FramesFactory.getEME2000()
        a = (self.perigee + self.apogee + (2*Constants.WGS84_EARTH_EQUATORIAL_RADIUS)) / 2
        e = 1.0 - (self.perigee + Constants.WGS84_EARTH_EQUATORIAL_RADIUS) / a
        self.orbit = KeplerianOrbit(
            a,
            e,
            self.inclination,
            self.arg_of_periapsis,
            self.raan,
            self.initial_lv,
            PositionAngleType.TRUE,
            self.inertial_frame,
            self.initial_date,
            Constants.WGS84_EARTH_MU
        )

    def get_orbit(self):
        return self.orbit


class OrbitPropagator:
    def __init__(self, orbit, propagation_parameters):
        self.orbit = orbit
        self.initial_time = propagation_parameters['initial_date']
        self.current_time = propagation_parameters['initial_date']
        self.final_time = propagation_parameters['final_date']
        self.timestep = propagation_parameters['timestep']
        self.propagator = KeplerianPropagator(self.orbit)

    def propagate_orbit(self):
        state_history = []
        while self.current_time.compareTo(self.final_time) < 1:
            current_state = self.propagator.propagate(self.current_time)
            state_history.append(current_state)
            self.current_time = self.current_time.shiftedBy(self.timestep)
        return state_history
