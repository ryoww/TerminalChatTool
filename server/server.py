from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

userinfos = {}
rooms = ['Open']

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('request_username')

@socketio.on('register_username')
def handle_register_username(data):
    sid = request.sid
    username = data.get('username')
    userinfos[sid] = {'name' : username}
    print(userinfos)
    emit('response', {'message' : f'Welcom, {username}!'})


@socketio.on('rooms')
def handle_rooms():
    rooms_counts = []

    for room in rooms:
        count = sum(1 for user in userinfos.values() if user['room'] == room)
        room_count = [room, count]
        rooms_counts.append(room_count)

    emit('view_rooms', {'rooms' : rooms_counts})




@socketio.on('message')
def handle_message(data):
    print('Received message', data)
    emit('response', {'message' : f'Server received: {data}'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', port=5000)