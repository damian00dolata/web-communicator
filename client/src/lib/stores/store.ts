import { writable } from "svelte/store";

//export const userId = writable();

let uid: number = 0;
let roomId: string = '';
let isRoomOpen: boolean = false;

export const userId = writable(uid);
export const lastRoomCreatedId = writable(roomId);
export const isRoomOpened = writable(isRoomOpen);