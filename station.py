from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import pyproj
import math

class Station:
    def __init__(self, id, lat, long, alt, size=15):
        self.id = id
        self.lat = lat
        self.long = long
        self.alt = alt
        self.size = size
        self.ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        self.lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

    def get_ecef_position(self):
       return pyproj.transform(self.lla, self.ecef, self.long, self.lat, self.alt, radians=False)

    def get_position(self):
        return {'latitude': self.lat, 'longitude': self.long, 'height': self.alt, 'size': self.size, 'id': self.id}
