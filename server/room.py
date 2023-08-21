import uuid
from message import Message

class Room:
	def __init__(self, roomName, maxUsers, isTemporary):
		self.roomId = str(uuid.uuid4())
		self.roomName: str = roomName
		self.currentUsers: str = []
		self.maxUsers: int = maxUsers
		self.isTemporary: bool = isTemporary
		self.messages: Message = []
	
	def deleteRoom(self, roomId):
		for i in range(len(roomList)):
			if roomList[i].roomId == roomId:
				del roomList[i]

roomList: Room = []