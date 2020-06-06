# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
import time
from flask import Response
from flask import Flask
from flask import render_template
from flask import jsonify
from engineio import payload
from flask_socketio import SocketIO, send, emit
payload.Payload.max_decode_packets = 500
VERBOSITY = 1
DEBUGLEVEL = 1
remotes = []
screens = []
remotes_inc = 0
screens_inc = 0
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


@socketio.on('addNewTeam', namespace='/remote')
def ws_addNewTeam(message):
    print('addNewTeam' + str(message['data']))
    emit('addNewTeam', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('addNewPlayer', namespace='/remote')
def ws_addNewPlayer(message):
    print('addNewPlayer' + str(message['data']))
    emit('addNewPlayer', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('options_roundTime', namespace='/remote')
def ws_set_options_roundTime(message):
    print('set_options_roundTime' + str(message['data']))
    emit('options_roundTime', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('guessed', namespace='/remote')
def ws_guessed(message):
    print('guessed' + str(message['data']))
    emit('guessed', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('pointGoesTo', namespace='/remote')
def ws_pointGoesTo(message):
    print('pointGoesTo' + str(message['data']))
    emit('pointGoesTo', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('next_player', namespace='/remote')
def ws_nextplayer(message):
    print('next_player' + str(message['data']))
    emit('next_player', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('guessedPause', namespace='/remote')
def ws_guessedPause(message):
    print('guessedPause' + str(message['data']))
    emit('guessedPause', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('resetClock', namespace='/remote')
def ws_resetClock(message):
    print('resetClock' + str(message['data']))
    emit('resetClock', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('showNextPlayerMessage', namespace='/remote')
def ws_showNextPlayerMessage(message):
    print('showNextPlayerMessage' + str(message['data']))
    emit('showNextPlayerMessage', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('nextPlayerConfirmed', namespace='/remote')
def ws_nextPlayerConfirmed(message):
    print('nextPlayerConfirmed' + str(message['data']))
    emit('nextPlayerConfirmed', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('resetClock', namespace='/remote')
def ws_resetClock(message):
    print('resetClock' + str(message['data']))
    emit('resetClock', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('pause', namespace='/remote')
def ws_pause(message):
    print('pause' + str(message['data']))
    emit('pause', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('unpause', namespace='/remote')
def ws_pause(message):
    print('unpause' + str(message['data']))
    emit('unpause', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('clearCanvas', namespace='/remote')
def ws_clearCanvas(message):
    print('clearCanvas' + str(message['data']))
    emit('clearCanvas', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('send_clear', namespace='/remote')
def ws_send_clear(message):
    print('send_clear' + str(message['data']))
    emit('send_clear', {'data': message['data']},
         namespace='/screen', broadcast=True)


@socketio.on('player_drawn_new_line', namespace='/remote')
def ws_program(message):
    #print('Message: ' + str(message['data']))
    emit('display_drawn_line', {
         'data': message['data']}, namespace='/screen', broadcast=True)


@socketio.on('clear', namespace='/remote')
def ws_program(message):
    print('clear')
    emit('clear', {'data': 'clear'},  namespace='/screen', broadcast=True)


@socketio.on('game_started', namespace='/remote')
def ws_program(message):
    print('game started ')
    game_started = True


@socketio.on('connect', namespace='/screen')
def ws_connect_screen():
    global screens_inc
    # if somebody accidentally gets disconnected  we need to keep copy of all drawn and deleted dots?
    screens_inc += 1

    print('screen connected')
    emit('welcome_new_screen', {'data': screens_inc},
         namespace="/remote", broadcast=True)
    emit('welcome_new_screen', {'data': screens_inc},
         namespace="/screen", broadcast=True)


@socketio.on('full_state', namespace='/screen')
def ws_full_state():
    global screens
    # if somebody accidentally gets disconnected  we need to keep copy of all drawn and deleted dots?
    print('full_state_requested')
    emit('full_state_request', {'data': now_timestamp()})


@socketio.on('connect', namespace='/remote')
def ws_connect_remote():
    global remotes_inc
    # TODO do not accept more connections, reject connections
    # google for rejecting new connections
    # TODO google restrict amount of connections
    # if somebody accidentally gets disconnected  we need to keep copy of all drawn and deleted dots?
    remotes_inc += 1
    print('Client connected')
    emit('welcome_new_remote', {'data': remotes_inc},
         namespace="/screen", broadcast=True)
    emit('welcome_new_remote', {'data': remotes_inc},
         namespace="/remote", broadcast=True)


@socketio.on('disconnect', namespace='/remote')
def ws_disconnect_remote():
    global remotes_inc
    print('remote disconnected')
    remotes_inc -= 1
    emit('remote_disconnected', {'data': remotes_inc},
         namespace="/remote", broadcast=True)
    emit('remote_disconnected', {'data': remotes_inc},
         namespace="/screen", broadcast=True)


@socketio.on('disconnect', namespace='/screen')
def ws_disconnect_screen():
    global screens_inc
    print('screen disconnected')
    screens_inc -= 1
    emit('screen_disconnected', {'data': screens_inc},
         namespace="/remote", broadcast=True)
    emit('screen_disconnected', {'data': screens_inc},
         namespace="/screen", broadcast=True)


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
