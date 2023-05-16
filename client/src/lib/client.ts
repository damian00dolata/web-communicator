import { Socket, io } from "socket.io-client";
import { RoomList } from "./global/roomList";
import { ClientList } from "./global/clientList";

class Client {
  private clientName: string;
  private clientSocket: any = {};

  constructor(clientName?: string, clientSocket?: any) {
    this.clientName = (clientName? clientName : '');
    this.clientSocket = (clientSocket? clientSocket : Socket.prototype);
    //this.clientName = '';
    //this.clientSocket = Socket.prototype;
  }

  private setUpEvents() {
    this.clientSocket.on('connect', () => {
      console.log('connected');
    });

    this.clientSocket.on('disconnect', () => {
      console.log('disconnected');
    });

    this.clientSocket.on('roomCreated', (e: any) => {
      RoomList.getInstance().setRoomList(e);
    });

    this.clientSocket.on('clientCreated', (e: any) => {
      ClientList.getInstance().setClientList(e);
    });
  }

  public createSocket() {
    this.clientSocket = io('http://localhost:8000');
    this.setUpEvents();
  }

  public setClientName(clientName: string) {
    this.clientName = clientName;
  }

  public getClientName() {
    return this.clientName;
  }

  public getClientSocket() {
    return this.clientSocket;
  }
}

export { Client }