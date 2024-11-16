from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
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
    join_room('Open')
    userinfos[sid] = {'name' : username, 'room' : 'Open'}
    print(userinfos)
    emit('response', {'message' : f'Welcom, {username}!'})
    emit('response', {'message' : f'{username} has joined the chat.'}, room='Open', include_self=False)


@socketio.on('create_room')
def handle_create_room(data):
    sid = request.sid
    room = data.get('room_name')
    if room not in rooms:
        rooms.append(room)
        previous_room = userinfos[sid]['room']
        leave_room(previous_room)
        join_room(room)
        userinfos[sid]['room'] = room
        emit('response', {'message' : f'Room "{room}" created and joined.'})

    else:
        emit('response', {'message' : f'Room "{room}" does not exist.'})


@socketio.on('join_room')
def handle_join_room(data):
    sid = request.sid
    room = data.get('room')
    
    if room in rooms:
        previous_room = userinfos[sid]['room']
        leave_room(previous_room)
        join_room(room)
        userinfos[sid]['room'] = room
        username = userinfos[sid]['name']
        emit('response', {'message' : f'You have joined room "{room}"'})
        emit('response', {'message' : f'{username} has joined the room.'}, room=room, include_self=False)
        
    else:
        emit('response', {'message' : f'Room "{room}" does not exist.'})

    print('join_room')


@socketio.on('leave_room')
def handle_leave_room():
    sid = request.sid
    room = userinfos[sid]['room']
    if room != 'Open':
        leave_room(room)
        join_room('Open')
        username = userinfos[sid]['name']
        emit('response', {'message' : f'You have left room "{room}".'})
        emit('response', {'message' : f'{username} has left the room.'}, room=room, include_self=False)
        
        remaining_users = [user for user in userinfos.values() if user['room'] == room]

        if not remaining_users:
            rooms.remove(room)
            print(f'Room "{room}" has been deleted because it is empty.')

    else:
        emit('response', {'message' : 'You cannot leave the "Open" chat.'})


@socketio.on('rooms')
def handle_rooms():
    rooms_counts = []

    for room in rooms:
        # 別にnamesは入れなくていい
        names = [user['name'] for user in userinfos.values() if user['room'] == room]
        count = sum(1 for user in userinfos.values() if user['room'] == room)
        room_count = [room, count, names]
        rooms_counts.append(room_count)

    emit('view_rooms', {'rooms' : rooms_counts})


@socketio.on('message')
def handle_message(data):
    sid = request.sid
    username = userinfos[sid]['name']
    text = data['text']
    room = userinfos[sid]['room']
    print('Received message', data)
    emit('response', {'message' : f'{username}: {text}'},room=room, include_self=False)


@socketio.on('disconnect')
def handle_exit():
    sid = request.sid
    if sid in userinfos:
        username = userinfos[sid]['name']
        room = userinfos[sid]['room']
        del userinfos[sid]
        emit('response', {'message' : f'Leave {username}'}, room=room)


if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', port=5000, debug=True)