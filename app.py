from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import time

app = Flask(__name__)
CORS(app)
params = {"ping_timeout": 60 * 60}
socketio = SocketIO(app, **params)

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


if __name__ == '__main__':
    socketio.run(app)
