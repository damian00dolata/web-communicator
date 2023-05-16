class Room {
  roomName: string;
  currentUsers: number;
  maxUsers: number;

  constructor(roomName: string, currentUsers: number, maxUsers: number) {
    this.roomName = roomName;
    this.currentUsers = currentUsers;
    this.maxUsers = maxUsers;
  }
}

export { Room }