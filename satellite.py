from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import pyproj
import math

class Satellite:
    def __init__(self, id, line1, line2, size=10):
        self.satellite = twoline2rv(line1, line2, wgs84)
        self.id = id
        self.size = size
        self.scale = 10
        self.ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        self.lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        self.a = self._get_semi_major_axis(line2[52:63])

    def get_propagation(self, time):
        position, velocity = self.satellite.propagate(time.year, time.month, time.day, time.hour, time.minute,
                                                      time.second)
        return position, velocity

    def get_position(self, time):
        position, velocity = self.get_propagation(time)
        longitude, latitude, radius = pyproj.transform(self.ecef, self.lla, position[0] * 1000, position[1] * 1000, position[2] * 1000, radians=False)
        if math.isnan(longitude) or math.isnan(latitude) or math.isnan(radius):
            return None
        return {'latitude': latitude, 'longitude': longitude, 'height': radius, 'size': self.size, 'id': self.id}

    def _get_semi_major_axis(self, n):
        return (math.pow(3.986004418e14, 1/3)) / (math.pow((2 * float(n) * math.pi / 86400), 2/3))

    def get_semi_major_axis(self):
        return self.a

    def set_size(self, size):
        self.size = size