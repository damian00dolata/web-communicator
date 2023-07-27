import json
import socketio

import room
from room import Room
import client
import message as mess

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
  newClientList = [client for client in client.clientList if client.clientSid != sid]
  client.clientList = newClientList

@sio_server.event
async def addRoom(sid, data):
  print(f'Received {data} of type {type(data)}')
  data = json.loads(data)
  _room = room.Room(data["roomName"], data["currentUsers"], data["maxUsers"], data["roomOwner"])
  room.roomList.append(_room)
  print(_room.roomId)
  #jsonStr = json.dumps([obj.__dict__ for obj in room.roomList])
  #print(f'{jsonStr} of type {type(jsonStr)}')
  await generateRoomList(sid)
  await sio_server.emit('roomCreated', _room.roomId)

@sio_server.event
async def addClient(sid, data):
  print(f'Received {data} of type {type(data)}')
  clientId = int(len(client.clientList)) + 1
  _client = client.Client(clientId, data, sid)
  client.clientList.append(_client)
  jsonStr = json.dumps([obj.__dict__['clientName'] for obj in client.clientList])
  print(f'{jsonStr} of type {type(jsonStr)}')
  print('clientId: ', clientId)
  await generateClientId(sid, clientId)
  await sio_server.emit('clientCreated', jsonStr)

@sio_server.event
async def generateClientId(sid, clientId):
  await sio_server.emit('userIdGenerated', clientId, to=sid)

@sio_server.event
async def joinedRoom(sid, roomId, clientId):
  print(clientId, " joined ", roomId)
  for r in room.roomList:
    if r.roomId == roomId:
      r.currentUsers += 1
      break
  await generateRoomList(sid)
  #await sio_server.emit('clientCreated', jsonStr)

@sio_server.event
async def leftRoom(sid, roomId):
  #print("someone has left the room", roomId)
  for r in room.roomList:
    if r.roomId == roomId:
      r.currentUsers -= 1
      print("Current users of room ", r.roomName, ": ", r.currentUsers)
      if r.currentUsers == 0:
        print("Removing ", r.roomName, "...")
        r.deleteRoom(roomId)
      break
  await generateRoomList(sid)

@sio_server.event
async def sendMessage(sid, clientName, message, roomId):
  _message = mess.Message(clientName, message)
  for r in room.roomList:
    if r.roomId == roomId:
      r.messages.append(_message)
      jsonStr = json.dumps([obj.__dict__ for obj in r.messages])
  print("messages: ", jsonStr)
  
  #await sio_server.emit('returnMessageList', jsonStr)

@sio_server.event
async def generateRoomList(sid):
  jsonStr = json.dumps([obj.__dict__ for obj in room.roomList])
  await sio_server.emit('sendRoomList', jsonStr)

# @sio_server.event
# async def chat(sid, message):
#   await sio_server.emit('chat', {'sid': sid, 'message': message})