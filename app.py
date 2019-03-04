from datetime import datetime, timedelta

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import time
import random
import logging
import math

from satellite import Satellite

app = Flask(__name__)
CORS(app)
params = {"ping_timeout": 60 * 60}
socketio = SocketIO(app, **params)
logging.basicConfig(filename='B:\\UCCS\\Web\\cs5260\\server\\satellite.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

@app.route('/')
def hello_world():
    return render_template('index.html')

@socketio.on('points')
def points():
    lat = 0
    long = 0
    while True:
        point = {'name': 'test1', 'longitude': lat, 'latitude': long, 'height': 1000000, 'size': 10}
        socketio.emit('points', point)
        print('sent point')
        lat = lat + 1
        long = long + 1
        time.sleep(10)

def rand_lat():
    return random.randint(0, 90)

def rand_long():
    return random.randint(0, 180)

def rand_height():
    return random.randint(3000000, 5000000)

sats = []
line1 = '1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753'
line2 = '2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667'
sat1 = Satellite(id='sat1', size=10, line1=line1, line2=line2)
sats.append(sat1)
tleLine1 = '1 25544U 98067A   13149.87225694  .00009369  00000-0  16828-3 0  9031'
tleLine2 = '2 25544 051.6485 199.1576 0010128 012.7275 352.5669 15.50581403831869'
sat2 = Satellite(id='sat2', size=10, line1=tleLine1, line2=tleLine2)
sats.append(sat2)
tl1 = '1 17181U 86096A   19061.54477344 -.00000327  00000-0  00000+0 0  9994'
tl2 = '2 17181  14.6347   0.1098 0002456 287.7661 168.6772  1.00266807125563'
sat3 = Satellite(id='sat3', size=10, line1=tl1, line2=tl2)
sats.append(sat3)

def line(satells, time):
    dist = distance(satells[0].get_propagation(time)[0], satells[1].get_propagation(time)[0])
    logging.debug('Distance [{}]'.format(dist))
    if dist <= 10000000:
        return True
    return False

def distance(p_1, p_2):
    return math.sqrt(math.pow(p_1[0] - p_2[0], 2) + math.pow(p_1[1] - p_2[1], 2) + math.pow(p_1[2] - p_2[2], 2)) * 1000

@socketio.on('satellite')
def satellite(clock_time):
    strptime = datetime.strptime(clock_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    sats_ = [x.get_position(strptime) for x in sats]
    socketio.emit('satellite', {'satellites': sats_, 'lines': False})
    time.sleep(1/100)

if __name__ == '__main__':
    socketio.run(app)
