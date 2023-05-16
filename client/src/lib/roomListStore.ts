import { writable } from "svelte/store";
import type { Room } from "./room";

let availableRooms: Array<Room> = new Array();
export const roomList = writable(availableRooms);