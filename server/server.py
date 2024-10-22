import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    # 接続されたクライアントを登録
    connected_clients.add(websocket)
    try:
        # メッセージを受信してブロードキャスト
        async for message in websocket:
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    finally:
        # クライアントの登録を解除
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # 無限に実行

asyncio.run(main())
