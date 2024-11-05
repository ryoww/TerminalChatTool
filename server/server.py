from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'message' : 'Welcome to the server'})

@socketio.on('message')
def handle_message(data):
    print('Received message', data)
    emit('response', {'message' : f'Server received: {data}'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', port=5000)