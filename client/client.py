import socketio

from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.table import Table

from key import URL

console = Console()


sio = socketio.Client()

# 部屋選択中かどうかを示すフラグ
is_handle_rooms = False

is_username_set = False

now_room_name = 'Open'

first_prompt_printed = False

def room_banner(room_name):
    gradient_text = Text(f'Welcome to {room_name} Chat !!', style='bold #DAF7A6')
    
    banner = Panel(
        Align.center(gradient_text),
        border_style='bold magenta',
        title='TerminalChatTool',
        title_align='left'
    )
    console.print(banner)


@sio.on('request_username')
def request_username():
    console.clear()
    
    room_banner(now_room_name)
    
    global is_username_set
    global username
    
    # while not is_username_set:
    username = console.input('[bold magenta]Enter your username[/bold magenta]\n')
    sio.emit('register_username', {'username': username})



@sio.on('view_rooms')
def view_rooms(data):
    global is_handle_rooms
    global now_room_name
    console.clear()
    
    list_rooms = data['rooms']
    rooms_len = len(list_rooms)

    # オプションを追加
    list_rooms.append(['Create and join room'])
    list_rooms.append(['Back'])

    
    table = Table(
        title_style='cyan',
        border_style='bright_blue', 
        style='cyan'
    )
    
    table.add_column('num', justify='center')
    table.add_column("room's name", justify='center')
    
    # 各部屋情報をテーブルに追加
    for index, room_info in enumerate(list_rooms, 1):
        room_name = room_info[0] if isinstance(room_info, list) and room_info else room_info
        table.add_row(str(index), str(room_name))
    
    panel = Panel(
        Align.center(table),
        title='Choose a room',
        # title_style='bold blue',
        title_align='center',
        border_style='bright_blue'
    )

    console.print(panel)

    while True:
        try:
            room_num = int(console.input(f'[bold yellow]Please select a room or command (1 ~ {rooms_len + 2}): [/bold yellow]')) - 1

            if 0 <= room_num < rooms_len:
                # 部屋に参加
                room_name = list_rooms[room_num][0] if isinstance(list_rooms[room_num], list) else list_rooms[room_num]
                sio.emit('join_room', {'room': room_name})
                break
            elif room_num == rooms_len:
                # 新しい部屋を作成
                while True:
                    new_room_name = console.input('[bold yellow]Please enter new room name: [/bold yellow]')
                    if new_room_name and new_room_name not in [room[0] for room in list_rooms if isinstance(room, list)]:
                        sio.emit('create_room', {'room_name': new_room_name})
                        console.clear()
                        room_banner(new_room_name)
                        now_room_name = new_room_name
                        break
                    else:
                        console.print('Invalid room name or room already exists.', style='bold magenta')
                break
            elif room_num == rooms_len + 1:
                # 戻る
                break
            else:
                console.print('Invalid selection.', style='bold magenta')
        except ValueError:
            console.print('Error: Please enter a valid integer.', style='bold magenta')
    # 部屋選択が完了したのでフラグを下げる
    is_handle_rooms = False



@sio.on('response')
def on_response(data):
    global is_username_set
    message = data['message']
    msg = Text()
    # msg.append('\n')
    
    if data['sender'] == 'system':
        align = 'left'
        msg.append(message, style='bold magenta')

    elif data['sender'] == 'user':
        align = 'right'
        msg.append(data['username'], style=data['color'])
        msg.append(data['message'])
    
    # msg.append('\n')
    aligned_msg = Align(msg, align=align)
    
    console.print(aligned_msg)
    
    if 'Welcom' in message:
        is_username_set = True


@sio.event
def disconnect():
    console.print('[bold magenta]Disconnected from the server[/bold magenta]')


sio.connect(URL)


try:
    while True:
        if not is_handle_rooms and is_username_set:
            if not first_prompt_printed:
                message = console.input(f"Enter a message (type 'exit' to quit)\n")
                first_prompt_printed = True
            else:
                message = console.input()
            
            if message.lower() == 'exit':
                if now_room_name != 'Open':
                    sio.emit('leave_room')
                sio.disconnect()
                break
            elif message == '/rooms':
                console.clear()
                is_handle_rooms = True
                sio.emit('rooms')
            elif message == '/leave_room':
                sio.emit('leave_room')
                console.clear()
                room_banner('Open')
            else:
                sio.emit('message', {'text': message})

except KeyboardInterrupt:
    print('\nClient terminated by user.\n')
    sio.emit('leave_room')
    sio.disconnect()
