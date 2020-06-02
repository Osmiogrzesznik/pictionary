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
game_started = False


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


@socketio.on('addNewTeam', namespace='/player')
def ws_addNewTeam(message):
    print('addNewTeam' + str(message['data']))
    emit('addNewTeam', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('addNewPlayer', namespace='/player')
def ws_addNewPlayer(message):
    print('addNewPlayer' + str(message['data']))
    emit('addNewPlayer', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('options_roundTime', namespace='/player')
def ws_set_options_roundTime(message):
    print('set_options_roundTime' + str(message['data']))
    emit('set_options_roundTime', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('guessed', namespace='/player')
def ws_guessed(message):
    print('guessed' + str(message['data']))
    emit('guessed', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('pointGoesTo', namespace='/player')
def ws_pointGoesTo(message):
    print('pointGoesTo' + str(message['data']))
    emit('pointGoesTo', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('next_player', namespace='/player')
def ws_nextplayer(message):
    print('nextplayer' + str(message['data']))
    emit('nextplayer', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('showNextPlayerMessage', namespace='/player')
def ws_showNextPlayerMessage(message):
    print('showNextPlayerMessage' + str(message['data']))
    emit('showNextPlayerMessage', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('resetClock', namespace='/player')
def ws_resetClock(message):
    print('resetClock' + str(message['data']))
    emit('resetClock', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('showNextPlayerMessage', namespace='/player')
def ws_showNextPlayerMessage(message):
    print('showNextPlayerMessage' + str(message['data']))
    emit('showNextPlayerMessage', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('nextPlayerConfirmed', namespace='/player')
def ws_nextPlayerConfirmed(message):
    print('nextPlayerConfirmed' + str(message['data']))
    emit('nextPlayerConfirmed', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('resetClock', namespace='/player')
def ws_resetClock(message):
    print('resetClock' + str(message['data']))
    emit('resetClock', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('pause', namespace='/player')
def ws_pause(message):
    print('pause' + str(message['data']))
    emit('pause', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('clearCanvas', namespace='/player')
def ws_clearCanvas(message):
    print('clearCanvas' + str(message['data']))
    emit('clearCanvas', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('send_clear', namespace='/player')
def ws_send_clear(message):
    print('send_clear' + str(message['data']))
    emit('send_clear', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('player_drawn_new_line', namespace='/player')
def ws_program(message):
    print('Message: ' + str(message['data']))
    emit('display_drawn_line', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('clear', namespace='/player')
def ws_program(message):
    print('clear')
    emit('clear', {'data': 'clear'},  namespace='/screen', broadcast=True)


@socketio.on('game_started', namespace='/player')
def ws_program(message):
    print('game started ')
    game_started = True


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
    if game_started:
        # TODO do not accept more connections, reject connections
        # google for rejecting new connections
        # TODO google restrict amount of connections
        # if somebody accidentally gets disconnected  we need to keep copy of all drawn and deleted dots?
        clients.append(now_timestamp())
    print('Client connected')
    emit('welcome_new_player', {'data': len(clients)}, namespace="/screen")


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
