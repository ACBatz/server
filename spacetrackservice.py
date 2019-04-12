import requests
import logging
import datetime

from satellite import Satellite

# logging.basicConfig(filename='satellite.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

class SatelliteTrackService:
    def __init__(self):
        response = requests.get('http://www.celestrak.com/NORAD/elements/active.txt')
        splits = response.content.decode('utf-8').split('\r\n')
        pass

    @staticmethod
    def get_satellite_data():
        response = open('active.txt', 'r').readlines()
        splits = response
        satellites = []
        size = 10
        for i in range(0, len(splits) - 1, 3):
            satellite = Satellite(id=splits[i].replace(' ', '').replace('\n', ''), line1=splits[i+1].replace('\n', ''), line2=splits[i+2].replace('\n', ''), size=size)
            satellites.append(satellite)
        satellites.sort(key=lambda x: x.get_semi_major_axis())
        satellites = satellites[:1250 if len(satellites) >= 1250 else len(satellites)]
        print('Retrieved [{}] satellites from Celestrak'.format(len(satellites)))
        return satellites