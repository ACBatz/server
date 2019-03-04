from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import math
import logging

class Satellite:
    def __init__(self, id, size, line1, line2):
        self.satellite = twoline2rv(line1, line2, wgs72)
        self.id = id
        self.size = size
        self.scale = 10

    def get_propagation(self, time):
        position, velocity = self.satellite.propagate(time.year, time.month, time.day, time.hour, time.minute,
                                                      time.second)
        return position, velocity

    def get_position(self, time):
        # position, velocity = self.satellite.propagate(time['year'], time['month'], time['day'], time['hour'], time['minute'], time['second'])
        position, velocity = self.get_propagation(time)
        radius = math.sqrt(math.pow(position[0], 2) + math.pow(position[1], 2) + math.pow(position[2], 2)) * 1000
        polar = math.acos(position[2] / radius)
        azimuth = math.atan2(position[1], position[0])

        latitude = math.degrees(polar - math.radians(90))
        longitude = math.degrees(azimuth)

        # logging.debug('time [{}, {}, {}, {}, {}, {}'.format(time.year, time.month, time.day, time.hour, time.minute, time.second))
        # logging.debug('position [{},{},{}]'.format(position[0], position[1], position[2]))

        return {'latitude': latitude, 'longitude': longitude, 'height': radius, 'size': self.size, 'id': self.id}

