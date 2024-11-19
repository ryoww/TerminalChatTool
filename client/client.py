import socketio
import threading

sio = socketio.Client()

# 部屋選択中かどうかを示すイベントフラグを作成
rooms_event = threading.Event()

@sio.on('request_username')
def request_username():
    username = input('Enter your username\n')
    sio.emit('register_username', {'username': username})

@sio.on('view_rooms')
def view_rooms(data):
    list_rooms = data['rooms']
    rooms_len = len(list_rooms)

    # オプションを追加
    list_rooms.append(['Create and join room', 0, []])
    list_rooms.append(['Back', 0, []])

    for index, room_info in enumerate(list_rooms, 1):
        room_name = room_info[0]
        print(f'{index}: {room_name}')

    while True:
        try:
            room_num = int(input(f'Please select a room or command (1 ~ {rooms_len + 2}): ')) - 1

            if 0 <= room_num < rooms_len:
                # 部屋に参加
                room_name = list_rooms[room_num][0]
                sio.emit('join_room', {'room': room_name})
                break
            elif room_num == rooms_len:
                # 新しい部屋を作成
                while True:
                    new_room_name = input('Please enter new room name: ')
                    if new_room_name and new_room_name not in [room[0] for room in list_rooms]:
                        sio.emit('create_room', {'room_name': new_room_name})
                        break
                    else:
                        print('Invalid room name or room already exists.')
                break
            elif room_num == rooms_len + 1:
                # 戻る
                break
            else:
                print('Invalid selection.')
        except ValueError:
            print('Error: Please enter a valid integer.')
    # 部屋選択が完了したのでイベントをセット
    rooms_event.set()

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
            sio.emit('leave_room')
            sio.disconnect()
            break
        elif message == '/rooms':
            # 部屋選択イベントをクリアして待機状態にする
            rooms_event.clear()
            sio.emit('rooms')
            # 部屋選択が完了するまで待機
            rooms_event.wait()
        elif message == '/leave_room':
            sio.emit('leave_room')
        else:
            sio.emit('message', {'text': message})

except KeyboardInterrupt:
    print('\nClient terminated by user.\n')
    sio.emit('leave_room')
    sio.disconnect()
