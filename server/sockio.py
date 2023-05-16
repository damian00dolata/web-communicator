import json
import socketio

import room
import client

sio_server = socketio.AsyncServer(
  async_mode='asgi',
  cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
  socketio_server=sio_server
  #socketio_path='sockio'
)

@sio_server.event
async def connect(sid, environ, auth):
  print(f'[Client {sid}] Connected!')

@sio_server.event
async def disconnect(sid):
  print(f'[Client {sid}] Disconnected!')

@sio_server.event
async def addRoom(sid, data):
  print(f'Received {data} of type {type(data)}')
  data = json.loads(data)
  _room = room.Room(data["roomName"], data["currentUsers"], data["maxUsers"])
  room.roomList.append(_room)
  jsonStr = json.dumps([obj.__dict__ for obj in room.roomList])
  print(f'{jsonStr} of type {type(jsonStr)}')
  await sio_server.emit('roomCreated', jsonStr)

@sio_server.event
async def addClient(sid, data):
  print(f'Received {data} of type {type(data)}')
  data = json.loads(data)
  _client = client.Client(data["clientName"], data["clientSocket"])
  client.clientList.append(_client)
  jsonStr = json.dumps([obj.__dict__ for obj in client.clientList])
  print(f'{jsonStr} of type {type(jsonStr)}')
  await sio_server.emit('clientCreated', jsonStr)

# @sio_server.event
# async def chat(sid, message):
#   await sio_server.emit('chat', {'sid': sid, 'message': message})