import uuid
from message import Message

class Room:
    def __init__(self, roomName, currentUsers, maxUsers, roomOwner):
        self.roomId = str(uuid.uuid4())
        self.roomName: str = roomName
        self.currentUsers: int = currentUsers
        self.maxUsers: int = maxUsers
        self.roomOwner: int = roomOwner
        self.messages: Message = []
    
    def deleteRoom(self, roomId):
        for i in range(len(roomList)):
            if roomList[i].roomId == roomId:
                del roomList[i]

    # def __str__(self):
    #     for r in roomList:
    #         return f'[Room name: {r.roomName}, current users: {r.currentUsers}, max users: {r.maxUsers}]\n'
roomList: Room = []