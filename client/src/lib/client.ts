import { Socket, io } from "socket.io-client";
import { RoomList } from "./global/roomList";
import { ClientList } from "./global/clientList";
import { userId, lastRoomCreatedId, isRoomOpened } from "./stores/store";
import { get } from 'svelte/store';


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
      //RoomList.getInstance().setRoomList(e);
      lastRoomCreatedId.set(e);
      this.clientSocket.emit('joinedRoom', e, get(userId));
      isRoomOpened.set(true);
    });

    this.clientSocket.on('clientCreated', (e: any) => {
      ClientList.getInstance().setClientList(e);
    });

    this.clientSocket.on('userIdGenerated', (e: any) => {
      userId.set(e);
      console.log("your id is: " + get(userId));
    });

    this.clientSocket.on('sendRoomList', (e: any) => {
      RoomList.getInstance().setRoomList(e);
    });

    // this.clientSocket.on('returnMessageList', (e: any, f: any) => {
    //   // userId.set(e);
    //   // console.log("your id is: " + get(userId));
    //   console.log("Messages: " + e);
    //   console.log("Room ID: " + f);
      
    // });
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