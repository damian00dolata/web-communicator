import { Socket, io } from "socket.io-client";
import { RoomList } from "./global/roomList";
import { ClientList } from "./global/clientList";
import { userId, lastRoomCreatedId, isRoomOpened } from "./stores/store";
import { get } from 'svelte/store';

const HOST = 'ws://localhost:8000';

class Client {
  private clientName: string;
  private clientSocket: any = {};

  constructor(clientName?: string, clientSocket?: any) {
    this.clientName = (clientName? clientName : '');
    this.clientSocket = (clientSocket? clientSocket : Socket.prototype);
  }

  private setUpEvents() {
    this.clientSocket.on('connect', () => {
      // console.log('connected');
    });

    this.clientSocket.on('disconnect', () => {
      // console.log('disconnected');
    });

    this.clientSocket.on('roomCreated', (e: any) => {
      lastRoomCreatedId.set(e);
      this.clientSocket.emit('joinedRoom', e, get(userId));
      isRoomOpened.set(true);
    });

    this.clientSocket.on('clientCreated', (e: any) => {
      ClientList.getInstance().setClientList(e);
    });

    this.clientSocket.on('userIdGenerated', (e: any) => {
      userId.set(e);
    });

    this.clientSocket.on('sendRoomList', (e: any) => {
      RoomList.getInstance().setRoomList(e);
    });
  }

  public createSocket() {
    this.clientSocket = io(`${HOST}`, {'path':'/ws/socket.io'});
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