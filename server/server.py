from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


userinfos = {}
rooms = ['Open']


def cleanup_room(room):
    remaining_users = [user for user in userinfos.values() if user['room'] == room]
    if not remaining_users and room != 'Open':
        rooms.remove(room)
        print(f'Room "{room}" has been deleted because it is empty.')


def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02X}{g:02X}{b:02X}'

@app.route('/')
def index():
    return {'status' : 'online'}


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('request_username')


@socketio.on('register_username')
def handle_register_username(data):
    sid = request.sid
    username = data.get('username')
    registered_usernames = [user['name'] for user in userinfos.values()]


    if not username:
        emit('response', {'message': 'Username cannot be empty.'})
        emit('request_username')


    elif username in registered_usernames:
        emit('response', {'message': f"The username '{username}' is already taken. Please choose a different one.", 'sender' : 'system'})
        emit('request_username')


    else:
        join_room('Open')
        user_color = generate_random_color()
        userinfos[sid] = {'name': username, 'room': 'Open', 'color': user_color}
        print(userinfos)
        emit('response', {'message': f'Welcome, {username}!', 'color': user_color, 'sender' : 'system'})
        emit('response', {'message': f'{username} has joined the chat.', 'color': user_color, 'sender' : 'system'}, room='Open', include_self=False)


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
        user_color = userinfos[sid]['color']
        emit('response', {'message': f'Room "{room}" created and joined.', 'color': user_color, 'sender' : 'system'})
    else:
        emit('response', {'message': f'Room "{room}" already exists.', 'sender' : 'system'})


@socketio.on('join_room')
def handle_join_room(data):
    sid = request.sid
    room = data.get('room')
    previous_room = userinfos[sid]['room']
    username = userinfos[sid]['name']
    user_color = userinfos[sid]['color']

    if room in rooms:
        if room != previous_room:
            leave_room(previous_room)
            join_room(room)
            userinfos[sid]['room'] = room
            emit('response', {'message': f'You have joined room "{room}"', 'sender' : 'system'})
            # emit('join_room', {'room_name' : room}, to=sid)
            emit('response', {'message': f'{username} has joined the room.', 'sender' : 'system'}, room=room, include_self=False)
        else:
            emit('response', {'message': f'You are in {previous_room} chat.', 'sender' : 'system'})
    else:
        emit('response', {'message': f'Room "{room}" does not exist.', 'sender' : 'system'})
    print('join_room')


@socketio.on('leave_room')
def handle_leave_room():
    sid = request.sid
    try:
        room = userinfos[sid]['room']
        username = userinfos[sid]['name']
        user_color = userinfos[sid]['color']

        if room != 'Open':
            leave_room(room)
            join_room('Open')
            userinfos[sid]['room'] = 'Open'
            emit('response', {'message': f'You have left room "{room}".', 'color': user_color, 'sender' : 'system'})
            emit('response', {'message': f'{username} has left the room.', 'color': user_color, 'sender' : 'system'}, room=room, include_self=False)
            cleanup_room(room)

        else:
            emit('response', {'message': 'You cannot leave the "Open" chat.', 'sender' : 'system'})

    except KeyError:
        emit('response', {'message': 'User information not found.', 'sender' : 'system'})


@socketio.on('rooms')
def handle_rooms():
    rooms_counts = []
    for room in rooms:
        # names = [user['name'] for user in userinfos.values() if user['room'] == room]
        # count = len(names)
        # room_info = [room, count, names]
        rooms_counts.append(room)
    emit('view_rooms', {'rooms': rooms_counts})


@socketio.on('message')
def handle_message(data):
    sid = request.sid
    try:
        username = userinfos[sid]['name']
        text = data.get('text', '')
        room = userinfos[sid]['room']
        user_color = userinfos[sid]['color']
        print('Received message', data)
        # 送信者本人以外に対してメッセージをブロードキャスト
        emit('response', {'message': f' : {text}', 'username' : username ,'color': f'bold {user_color}', 'sender' : 'user'}, room=room, include_self=False)
    except KeyError:
        emit('response', {'message': 'User information not found.', 'sender' : 'system'})


@socketio.on('disconnect')
def handle_exit():
    sid = request.sid
    if sid in userinfos:
        username = userinfos[sid]['name']
        room = userinfos[sid]['room']
        user_color = userinfos[sid]['color']
        del userinfos[sid]
        emit('response', {'message': f'{username} has disconnected.', 'color': user_color, 'sender' : 'system'}, room=room)
        cleanup_room(room)


if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', port=5000, debug=True)
