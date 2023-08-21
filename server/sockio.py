import json
import socketio
import room
from room import Room
import client
import message as mess
from roomReturn import RoomReturn
import httpx

class SockIO:
  def __init__(self) -> None:
    self.sio_server = socketio.AsyncServer(
      async_mode='asgi',
      cors_allowed_origins=[]
    )

    self.sio_app = socketio.ASGIApp(
      socketio_server=self.sio_server
    )

    @self.sio_server.event
    async def connect(sid, environ, auth):
      print(f'[Client {sid}] Connected!')

    @self.sio_server.event
    async def disconnect(sid):
      print(f'[Client {sid}] Disconnected!')

      clientId = await getClientIdBySid(sid)
      requests = httpx.AsyncClient()
      x = await requests.put(f'http://127.0.0.1:8000/user/changeStatus/{clientId}', headers={'accept':'application/json'}, timeout=5)
      await checkRooms(sid, clientId)
      newClientList = [client for client in client.clientList if client.clientSid != sid]
      client.clientList = newClientList

    @self.sio_server.event
    async def addRoom(sid, data):
      data = json.loads(data)
      _room = room.Room(data["roomName"], data["maxUsers"], data["isTemporary"])
      room.roomList.append(_room)
      
      if not (data["isTemporary"]):
        requests = httpx.AsyncClient()
        jsonData = {
            'roomId': _room.roomId,
            'name': data["roomName"],
            'maxUsers': data["maxUsers"],
            'isTemporary': data["isTemporary"]
        }
        x = await requests.post(f'http://127.0.0.1:8000/room/add', json=jsonData)
        
      await self.sio_server.emit('roomCreated', _room.roomId, to=sid)
      await generateRoomList(sid)

    @self.sio_server.event
    async def addClient(sid, data):
      requests = httpx.AsyncClient()
      x = await requests.get(f'http://127.0.0.1:8000/user/findByName/{data}', headers={'accept':'application/json'}, timeout=5)
      cli = json.loads(x.json())
      clientId = cli[0]

      x = await requests.put(f'http://127.0.0.1:8000/user/changeStatus/{clientId}', headers={'accept':'application/json'}, timeout=5)

      _client = client.Client(clientId, data, sid)
      client.clientList.append(_client)
      jsonStr = json.dumps([obj.__dict__['clientName'] for obj in client.clientList])
      await generateClientId(sid, clientId)
      await self.sio_server.emit('clientCreated', jsonStr)

    @self.sio_server.event
    async def generateClientId(sid, clientId):
      await self.sio_server.emit('userIdGenerated', clientId, to=sid)

    @self.sio_server.event
    async def joinedRoom(sid, roomId, clientId):
      for r in room.roomList:
        if r.roomId == roomId:
          r.currentUsers.append(clientId)
          break
      await generateRoomList(sid)

    @self.sio_server.event
    async def leftRoom(sid, roomId, clientId):
      for r in room.roomList:
        if r.roomId == roomId:
          if clientId in r.currentUsers:
            r.currentUsers.remove(clientId)
          if len(r.currentUsers) == 0 and r.isTemporary:
            r.deleteRoom(roomId)
          break
      await generateRoomList(sid)

    @self.sio_server.event
    async def sendMessage(sid, clientName, message, roomId):
      requests = httpx.AsyncClient()
      jsonData = {
          'clientName': clientName,
          'message': message,
          'roomId': roomId
      }

      x = await requests.post(f'http://127.0.0.1:8000/message/add', json=jsonData)
      await getMessages(sid, roomId)

    @self.sio_server.event
    async def getMessages(sid, roomId):
      requests = httpx.AsyncClient()
      x = await requests.get(f'http://127.0.0.1:8000/message/{roomId}', headers={'accept':'application/json'}, timeout=5)
      messages = json.loads(x.json())
      
      jsonStr = ''
      messToSend = []
      for message in messages:
        messToSend.append(mess.Message(message[0], message[1], message[2]))
      jsonStr = json.dumps([obj.__dict__ for obj in messToSend])
      await self.sio_server.emit('returnMessageList', data=(jsonStr, roomId))
      
    @self.sio_server.event
    async def generateRoomList(sid):
      requests = httpx.AsyncClient()
      x = await requests.get(f'http://127.0.0.1:8000/room', headers={'accept':'application/json'}, timeout=5)
      rooms = json.loads(x.json())
      
      dbRoomsIds = []
      for r in rooms:
        dbRoomsIds.append(r[1])
      memoryRoomsIds = []
      for r in room.roomList:
        memoryRoomsIds.append(r.roomId)
      roomDiff = set(dbRoomsIds).difference(memoryRoomsIds)
      for r in roomDiff:
        x = await requests.get(f'http://127.0.0.1:8000/room/getByRoomId/{r}', headers={'accept':'application/json'}, timeout=5)
        _r = json.loads(x.json())
        _room = room.Room(_r[2], _r[3], _r[4])
        _room.roomId = _r[1]
        room.roomList.append(_room)
      
      roomReturns: RoomReturn = []
      for r in room.roomList:
        _r = RoomReturn(r.roomId, r.roomName, len(r.currentUsers), r.maxUsers, r.isTemporary)
        roomReturns.append(_r)
      
      jsonStr = json.dumps([obj.__dict__ for obj in roomReturns])
      await self.sio_server.emit('sendRoomList', jsonStr)

    @self.sio_server.event
    async def getClientIdBySid(sid):
      clientId = 0
      for c in client.clientList:
        if c.clientSid == sid:
          clientId = c.clientId
          break
      return clientId

    @self.sio_server.event
    async def checkRooms(sid, clientId): # check for current users of room if socket is disconnected
      for r in room.roomList:
        if clientId in r.currentUsers:
          r.currentUsers.remove(clientId)
      await generateRoomList(sid)
