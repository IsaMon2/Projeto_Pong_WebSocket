import asyncio
import websockets


async def conectar():

    async with websockets.connect("ws://localhost:8080") as websocket:

        mensagem = await websocket.recv()

        print(mensagem)

        await websocket.send("Olá do jogador!")

        while True:

            mensagem = await websocket.recv()

            print("Recebi:", mensagem)

asyncio.run(conectar())