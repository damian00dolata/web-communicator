class Room {
  roomId: string;
  roomName: string;
  currentUsers: number;
  maxUsers: number;
  roomOwner: number;

  constructor(roomId: string, roomName: string, currentUsers: number, maxUsers: number, roomOwner: number) {
    this.roomId = roomId;
    this.roomName = roomName;
    this.currentUsers = currentUsers;
    this.maxUsers = maxUsers;
    this.roomOwner = roomOwner;
  }
}

export { Room }