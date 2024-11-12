import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to the server\n')
    

@sio.on('response')
def on_response(data):
    print('Received from server:\n', data['message'])

@sio.event
def disconnect():
    print('Disconnected from the server\n')

sio.connect('http://0.0.0.0:5000')

try:
    while True:
        message = input("Enter a message (type 'exit' to quit)\n")
        if message.lower() == 'exit':
            break
        sio.emit('message', {'text' : message})

except KeyboardInterrupt:
    print('\nClient terminated by user.\n')

sio.disconnect()