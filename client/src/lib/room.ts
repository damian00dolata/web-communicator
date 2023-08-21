class Room {
  roomId: string;
  roomName: string;
  currentUsers: number;
  maxUsers: number;
  isTemporary: number;

  constructor(roomId: string, roomName: string, currentUsers: number, maxUsers: number, isTemporary: number) {
    this.roomId = roomId;
    this.roomName = roomName;
    this.currentUsers = currentUsers;
    this.maxUsers = maxUsers;
    this.isTemporary = isTemporary;
  }
}

export { Room }