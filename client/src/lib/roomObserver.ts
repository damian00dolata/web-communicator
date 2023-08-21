import { RoomList } from "./global/roomList";
import type IObservable from "./interfaces/IObservable";
import type IObserver from "./interfaces/IObserver";
import type { Room } from "./room";

export class RoomObserver implements IObserver {
  public availableRooms: Array<Room> = new Array();
  
  public update(observable: IObservable): void {
    if (observable instanceof RoomList) {
      console.log('RoomObserver: Reacted to the event.');
      this.availableRooms = [];
      this.availableRooms = RoomList.getInstance().getRoomList();
      this.availableRooms = this.availableRooms;
    }
  }
}