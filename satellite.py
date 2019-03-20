from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import math
import pyproj
import logging

class Satellite:
    def __init__(self, id, size, line1, line2):
        self.satellite = twoline2rv(line1, line2, wgs84)
        self.id = id
        self.size = size
        self.scale = 10
        self.ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        self.lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

    def get_propagation(self, time):
        position, velocity = self.satellite.propagate(time.year, time.month, time.day, time.hour, time.minute,
                                                      time.second)
        return position, velocity

    def get_position(self, time):
        position, velocity = self.get_propagation(time)
        longitude, latitude, radius = pyproj.transform(self.ecef, self.lla, position[0] * 1000, position[1] * 1000, position[2] * 1000, radians=False)
        return {'latitude': latitude, 'longitude': longitude, 'height': radius, 'size': self.size, 'id': self.id}