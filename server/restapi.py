from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from dbase import Database
from sockio import SockIO
from routes.user import UserService
from routes.room import RoomService
from routes.message import MessageService
from models.user import User
from models.room import Room
from models.message import Message

class RestAPI:
  def __init__(self, dbInterface: Database, sioInterface: SockIO) -> None:
    self.app = FastAPI()
    self.app.mount('/ws', app=sioInterface.sio_app)
    self.db: Database = dbInterface

    self.app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @self.app.get("/")
    async def main():
      return {"message": "Hello world!"}

    @self.app.get("/user")
    async def getAllUsers():
      return await UserService.getAllUsers(self.db.conn)

    @self.app.get("/user/{_id}")
    async def findUserById(_id, response: Response):
      return await UserService.findById(self.db.conn, _id, response)
    
    @self.app.get("/user/findByName/{username}")
    async def findUserByName(username, response: Response):
      return await UserService.findByName(self.db.conn, username, response)
    
    @self.app.post("/user/register")
    async def addUser(user: User, response: Response):
      return await UserService.addUser(self.db.conn, user, response)
    
    @self.app.post("/user/login")
    async def authUser(user: User, response: Response):
      return await UserService.authUser(self.db.conn, user, response)
    
    @self.app.put("/user/{_id}")
    async def updateUser(user: User, _id, response: Response):
      return await UserService.updateUser(self.db.conn, user, _id, response)
    
    @self.app.delete("/user/{_id}")
    async def removeUser(_id, response: Response):
      return await UserService.removeUser(self.db.conn, _id, response)
    
    @self.app.put("/user/changeStatus/{_id}")
    async def changeStatus(_id, response: Response):
      return await UserService.changeStatus(self.db.conn, _id, response)


    @self.app.get("/room")
    async def getAllRooms():
      return await RoomService.getAllRooms(self.db.conn)
    
    @self.app.get("/room/{_id}")
    async def findRoomById(_id, response: Response):
      return await RoomService.findById(self.db.conn, _id, response)
    
    @self.app.get("/room/getByRoomId/{roomId}")
    async def findRoomByRoomId(roomId, response: Response):
      return await RoomService.findByRoomId(self.db.conn, roomId, response)
    
    @self.app.post("/room/add")
    async def addRoom(room: Room, response: Response):
      return await RoomService.addRoom(self.db.conn, room, response)
    
    @self.app.delete("/room/{_id}")
    async def removeRoom( _id, response: Response):
      return await RoomService.removeRoom(self.db.conn, _id, response)
    

    @self.app.get("/message/{_id}")
    async def getAllMessages(_id):
      return await MessageService.getAllMessages(self.db.conn, _id)
    
    @self.app.post("/message/add")
    async def addMessage(message: Message, response: Response):
      return await MessageService.addMessage(self.db.conn, message, response)
    
    @self.app.delete("/message/{roomId}")
    async def removeMessage(roomId, response: Response):
      return await MessageService.removeMessages(self.db.conn, roomId, response)