class Room:
    def __init__(self, roomName, currentUsers, maxUsers):
        self.roomName: str = roomName
        self.currentUsers: int = currentUsers
        self.maxUsers: int = maxUsers

    # def __str__(self):
    #     for r in roomList:
    #         return f'[Room name: {r.roomName}, current users: {r.currentUsers}, max users: {r.maxUsers}]\n'
roomList: Room = []