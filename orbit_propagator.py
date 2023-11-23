import math
from org.orekit.orbits import KeplerianOrbit, PositionAngleType
from org.orekit.propagation.analytical import KeplerianPropagator
from org.orekit.utils import Constants
from org.orekit.frames import FramesFactory

class OrbitCreator:
    def __init__(self, apogee, perigee, inclination, arg_of_periapsis, raan, initial_lv, initial_date): #TODO change to parameter object
        self.apogee = math.radians(apogee)
        self.perigee = math.radians(perigee)
        self.inclination = math.radians(inclination)
        self.arg_of_periapsis = math.radians(arg_of_periapsis)
        self.raan = math.radians(raan)
        self.initial_lv = math.radians(initial_lv)
        self.initial_date = initial_date
        self.current_date = initial_date #TODO duplication
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
            self.initial_date, #TODO check if this is initial date or  some sort of epoch date
            Constants.WGS84_EARTH_MU
        )

    def get_orbit(self):
        return self.orbit


class OrbitPropagator:
    def __init__(self, orbit, inital_date, final_date, timestep):
        self.orbit = orbit
        self.initial_time = inital_date #TODO time/date mismatch
        self.current_time = inital_date
        self.final_time = final_date
        self.timestep = timestep
        self.propagator = KeplerianPropagator(self.orbit)

    def propagate_orbit(self):
        state_history = []
        while self.current_time.compareTo(self.final_time) < 1:
            current_state = self.propagator.propagate(self.current_time)
            state_history.append(current_state)
            self.current_time = self.current_time.shiftedBy(self.timestep)
        return state_history # TODO maybe we only need to return true anomaly from this?

