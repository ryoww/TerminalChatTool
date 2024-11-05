import asyncio
import websockets

connected_clients = {}  # ユーザー名とWebSocketの対応を保持

async def handler(websocket, path):
    # クライアントからユーザー名を受信
    username = await websocket.recv()
    connected_clients[username] = websocket
    print(f"{username} が接続しました。")

    try:
        # 接続中のユーザーリストを全クライアントに送信
        await send_user_list()

        # クライアントからのメッセージを処理
        async for message in websocket:
            if message.startswith('request:'):
                # チャットリクエストの処理
                target_username = message.split(':', 1)[1]
                if target_username in connected_clients:
                    target_ws = connected_clients[target_username]
                    # 目標ユーザーにリクエストを送信
                    await target_ws.send(f"request_from:{username}")
                else:
                    await websocket.send(f"ユーザー {target_username} は見つかりません。")
            elif message.startswith('response:'):
                # リクエストへの応答の処理
                parts = message.split(':', 2)
                requester = parts[1]
                response = parts[2]
                if requester in connected_clients:
                    requester_ws = connected_clients[requester]
                    await requester_ws.send(f"response_from:{username}:{response}")
                    if response == 'yes':
                        # 個別チャットの開始
                        await start_private_chat(requester_ws, websocket, requester, username)
                        break  # ハンドラを終了
                else:
                    await websocket.send(f"ユーザー {requester} は見つかりません。")
            else:
                await websocket.send("無効なコマンドです。")

    finally:
        # クライアントの切断時にリストから削除
        del connected_clients[username]
        print(f"{username} が切断しました。")
        await send_user_list()

async def send_user_list():
    # 全クライアントにユーザーリストを送信
    user_list = ','.join(connected_clients.keys())
    for ws in connected_clients.values():
        await ws.send(f"user_list:{user_list}")

async def start_private_chat(ws1, ws2, user1, user2):
    # 個別チャットの開始を両ユーザーに通知
    await ws1.send(f"private_chat_with:{user2}")
    await ws2.send(f"private_chat_with:{user1}")

    async def forward_message(sender_ws, receiver_ws, sender_name):
        try:
            async for message in sender_ws:
                await receiver_ws.send(f"{sender_name}: {message}")
        except websockets.ConnectionClosed:
            await receiver_ws.send(f"{sender_name} が切断しました。")

    # 双方向のメッセージ転送を開始
    await asyncio.gather(
        forward_message(ws1, ws2, user1),
        forward_message(ws2, ws1, user2)
    )

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # 無限に実行

asyncio.run(main())
