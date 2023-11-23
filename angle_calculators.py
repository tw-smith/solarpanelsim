import math
from org.orekit.time import AbsoluteDate


class AngleCalculator:
    def __init__(self, spacecraft_state, keplerian_orbit): # TODO can we get RAAN from spacecraft state rather than having to import kep orbit?
        orbit = keplerian_orbit
        self.raan = orbit.getRightAscensionOfAscendingNode()
        self.inclination = orbit.getI()
        self.arg_of_periapsis = orbit.getPerigeeArgument()
        self.true_anomaly = spacecraft_state.getLv()
        self.obliquity = math.radians(23.45)
        # TODO is durationFrom correct here? Does it account for leap years etc? Check orekit docs
        seconds_since_J2000 = spacecraft_state.getDate().durationFrom(AbsoluteDate.J2000_EPOCH)
        self.days_since_J2000 = seconds_since_J2000 / 86400

    def get_sun_longitude(self):
        L = (280.466 + 0.9856474*self.days_since_J2000) % 360
        g = (357.528 + 0.9856003*self.days_since_J2000) % 360
        sun_longitude_degrees = L + 1.915*math.sin(math.radians(g)) + 0.02*math.sin(math.radians(2*g))
        return math.radians(sun_longitude_degrees)

    def get_beta_angle(self):
        sun_longitude = self.get_sun_longitude()
        return math.asin(
            math.cos(sun_longitude)*math.sin(self.raan)*math.sin(self.inclination) -
            math.cos(sun_longitude)*math.cos(self.obliquity)*math.cos(self.raan)*math.sin(self.inclination) +
            math.sin(sun_longitude)*math.sin(self.obliquity)*math.cos(self.inclination)
        )

    def get_satellite_true_longitude(self):
        return self.get_sun_longitude() + self.raan + self.true_anomaly
