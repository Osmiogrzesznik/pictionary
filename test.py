# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from flask import Response
from flask import Flask
from flask import render_template
from flask import jsonify
from engineio import payload
import time
from flask_socketio import SocketIO, send, emit
payload.Payload.max_decode_packets = 500
VERBOSITY = 1
DEBUGLEVEL = 1
clients = []
screens = []


def now_timestamp():
    return time.time() * 1000


def logD(msg):
    if VERBOSITY >= DEBUGLEVEL:
        print(msg)


# are viewing tthe stream)
# initialize a flask object
app = Flask(__name__)
socketio = SocketIO(app)

# only first screens receive dots and can send full mesh to newly connected
# only one player


@socketio.on('pdnd', namespace='/p')
def ws_program(message):
    print('Message: ' + str(message['data']))
    emit('dndl', {
         'data': message['data']}, namespace='/p', broadcast=True)


@socketio.on('connect', namespace='/screen')
def ws_connect_screen():
    global screens
    # if somebody accidentally gets disconnected  we need to keep copy of all drawn and deleted dots?
    screens.append(now_timestamp)

    print('screen connected')
    emit('welcome_new_screen', {'data': now_timestamp()})


@socketio.on('full_mesh', namespace='/screen')
def ws_full_mesh():
    global screens
    # if somebody accidentally gets disconnected  we need to keep copy of all drawn and deleted dots?
    screens.append(now_timestamp)

    print('screen connected')
    emit('welcome_new_screen', {'data': now_timestamp()})


@socketio.on('connect', namespace='/player')
def ws_connect():
    global clients
    # if somebody accidentally gets disconnected  we need to keep copy of all drawn and deleted dots?
    clients.append(now_timestamp())
    print('Client connected')
    emit('welcome_new_player', {'data': now_timestamp()})


@socketio.on('disconnect', namespace='/player')
def ws_disconnect():
    print('Client disconnected')


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # start the socketio and associated flask app
    socketio.run(app, host='0.0.0.0', port=8080,
                 debug=True, use_reloader=False)

# release the video stream pointer
print("finished!!!!!!!!"*99999)
