class RoomReturn:
  def __init__(self, roomId, roomName, currentUsers, maxUsers, isTemporary):
    self.roomId:str = roomId
    self.roomName: str = roomName
    self.currentUsers: int = currentUsers
    self.maxUsers: int = maxUsers
    self.isTemporary: bool = isTemporary