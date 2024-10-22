import asyncio
import websockets
import aioconsole

async def chat():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        username = await aioconsole.ainput("ユーザー名を入力してください: ")
        print("メッセージを入力してください。終了するには 'exit' と入力します。")
        
        async def receive_messages():
            while True:
                try:
                    message = await websocket.recv()
                    print(message)
                except websockets.ConnectionClosed:
                    print("サーバーとの接続が切れました。")
                    break
        
        async def send_messages():
            while True:
                message = await aioconsole.ainput()
                if message == "exit":
                    await websocket.close()
                    break
                await websocket.send(f"{username}: {message}")

        await asyncio.gather(receive_messages(), send_messages())

asyncio.run(chat())
