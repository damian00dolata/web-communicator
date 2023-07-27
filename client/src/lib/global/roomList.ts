import type IObservable from "$lib/interfaces/IObservable";
import type IObserver from "$lib/interfaces/IObserver";
import type { Room } from "../room";
import { roomList } from "../roomListStore";

class RoomList implements IObservable {
  private static instance: RoomList;

  private roomList: Array<Room> = new Array();
  private observers: IObserver[] = []; // unnecessary artifact

  private constructor() { }

  public static getInstance(): RoomList { // singleton
    if (!RoomList.instance) {
      RoomList.instance = new RoomList();
    }
    return RoomList.instance;
}

  public getRoomList(): Array<Room> {
    return this.roomList;
  }

  public setRoomList(availableRooms: string): void {
    this.roomList = [];

    var jsonData = JSON.parse(availableRooms);
    
    for (var i = 0; i < jsonData.length; i++) {
      var r = jsonData[i];
      this.roomList.push(r);
    }

    // this.notify();

    roomList.set(this.roomList);
  }

  public attach(observer: IObserver): void {
    const isExist = this.observers.includes(observer);
    if (isExist) {
      return console.log('Observable: Observer has been attached already.');
    }

    console.log('Observable: Attached an observer.');
    this.observers.push(observer);
  }

  public detach(observer: IObserver): void {
    const observerIndex = this.observers.indexOf(observer);
    if (observerIndex === -1) {
      return console.log('Observable: Nonexistent observer.');
    }

    this.observers.splice(observerIndex, 1);
    console.log('Observable: Detached an observer.');
  }

  public notify(): void {
    console.log('Observable: Notifying observers...');
    for (const observer of this.observers) {
      observer.update(this);
    }
  }

}

export { RoomList }