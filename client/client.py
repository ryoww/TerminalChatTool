import asyncio
import websockets
import aioconsole

async def chat():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        username = await aioconsole.ainput("ユーザー名を入力してください: ")
        await websocket.send(username)

        private_chat = False
        requester = None  # チャットリクエストを送ってきたユーザー名
        partner = None    # 個別チャット中の相手のユーザー名

        async def receive_messages():
            nonlocal private_chat, requester, partner
            while True:
                try:
                    message = await websocket.recv()
                    if message.startswith('user_list:'):
                        user_list = message.split(':', 1)[1]
                        print(f"接続中のユーザー: {user_list}")
                    elif message.startswith('request_from:'):
                        requester = message.split(':', 1)[1]
                        print(f"{requester} からチャットリクエストがあります。'yes' または 'no' で応答してください。")
                    elif message.startswith('response_from:'):
                        parts = message.split(':', 2)
                        responder = parts[1]
                        response = parts[2]
                        if response == 'yes':
                            print(f"{responder} がチャットリクエストを承認しました。")
                            private_chat = True
                            partner = responder
                        else:
                            print(f"{responder} がチャットリクエストを拒否しました。")
                    elif message.startswith('private_chat_with:'):
                        partner = message.split(':', 1)[1]
                        print(f"{partner} と個別チャットを開始しました。")
                        private_chat = True
                    else:
                        print(message)
                except websockets.ConnectionClosed:
                    print("サーバーから切断されました。")
                    break

        async def send_messages():
            nonlocal private_chat, requester, partner
            while True:
                message = await aioconsole.ainput()
                if message == 'exit':
                    await websocket.close()
                    break
                elif message == 'list':
                    # ユーザーリストは自動的に送信されるため何もしない
                    pass
                elif message.startswith('request '):
                    target = message.split(' ', 1)[1]
                    await websocket.send(f"request:{target}")
                elif message == 'yes' or message == 'no':
                    if requester:
                        await websocket.send(f"response:{requester}:{message}")
                        requester = None
                    else:
                        print("応答するチャットリクエストがありません。")
                else:
                    if private_chat:
                        await websocket.send(message)
                    else:
                        print("個別チャット中ではありません。'request <ユーザー名>' でチャットをリクエストしてください。")

        await asyncio.gather(receive_messages(), send_messages())

asyncio.run(chat())
