import socketio

sio = socketio.Client()


@sio.on('request_username')
def request_username():
    username = input('Enter your username\n')
    sio.emit('register_username', {'username' : username})

@sio.on('view_rooms')
def view_rooms(data):
    list_rooms = list(data['rooms'])
    rooms_len = len(list_rooms)
    list_rooms.extend(['Create and join room', 'Back'])
    
    for index, room in enumerate(list_rooms, 1):
        print(f'{index} : {room}')
    
    while True:
        try:
            room_num = int(input(f'Please select join room or command 1 ~ {rooms_len+2} : '))
            
            print('room_num : ', room_num)
            
            match room_num:
                case _ if  0 < room_num <= rooms_len:
                    sio.emit('join_room', {'room' : list_rooms[room_num][0]})
                    
                case _ if room_num == (rooms_len + 1):
                    while True:
                        new_room_name = input('Please enter new room name')
                        
                        if new_room_name and new_room_name not in list_rooms:
                            sio.emit('create_room', {'room_name' : new_room_name})
                            break
                        
                        else:
                            print('Invalid room name or room already exists')
                    break

                case _ if room_num == (rooms_len + 2):
                    break

        except ValueError:
            print('Error: Please enter a valid integer.')
    # print(type(list_rooms), list_rooms)
    

@sio.on('response')
def on_response(data):
    print(data['message'])

@sio.event
def disconnect():
    print('Disconnected from the server\n')

sio.connect('http://0.0.0.0:5000')

try:
    while True:
        message = input("Enter a message (type 'exit' to quit)\n")
        if message.lower() == 'exit':
            sio.disconnect()
            break
        elif message == '/rooms':
            sio.emit('rooms')
        elif message == '/leave_room':
            sio.emit('leave_room')
        else:
            sio.emit('message', {'text' : message})

except KeyboardInterrupt:
    print('\nClient terminated by user.\n')
    
    sio.disconnect()
    sio.wait()