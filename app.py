from datetime import datetime

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import logging
import math

from satellite import Satellite

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
# logging.basicConfig(filename='B:\\UCCS\\Web\\cs5260\\server\\satellite.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

@app.route('/')
def hello_world():
    return render_template('index.html')

sats = []
line1 = '1 25590U 98076A   19064.91273959  .00000018  00000-0  36015-5 0  9995'
line2 = '2 25590  82.9374  12.7710 0030482 304.3953 113.2645 13.72960770 11936'
sat1 = Satellite(id='sat1', size=10, line1=line1, line2=line2)
sats.append(sat1)
tleLine1 = '1 26818U 01023A   19064.84364637  .00000050  00000-0  37736-4 0  9997'
tleLine2 = '2 26818  82.9288  33.0547 0031430 254.5964 105.1727 13.73931458889587'
sat2 = Satellite(id='sat2', size=10, line1=tleLine1, line2=tleLine2)
sats.append(sat2)

def line(satells, time):
    dist = distance(satells[0].get_propagation(time)[0], satells[1].get_propagation(time)[0])
    if dist <= 3000000:
        return [{'id': '{}-{}'.format(satells[0].id, satells[1].id)}]
    return []

def distance(p_1, p_2):
    return math.sqrt(math.pow(p_1[0] * 1000 - p_2[0] * 1000, 2) + math.pow(p_1[1] * 1000 - p_2[1] * 1000, 2) + math.pow(p_1[2] * 1000 - p_2[2] * 1000, 2))

@app.route('/api/satellite',methods=['POST'])
def satellite():
    clock_time = request.get_json()['time']
    strptime = datetime.strptime(clock_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    sats_ = [x.get_position(strptime) for x in sats]
    l = line(sats, strptime)
    return jsonify({'satellites': sats_, 'lines': l})


if __name__ == '__main__':
    app.run()
