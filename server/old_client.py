import asyncio

import socketio

sio_client = socketio.AsyncClient()


@sio_client.event
async def connect():
    print('I\'m connected')


@sio_client.event
async def disconnect():
    print('I\'m disconnected')


async def main():
    await sio_client.connect(url='http://localhost:8000', socketio_path='sockio')
    await sio_client.disconnect()


asyncio.run(main())