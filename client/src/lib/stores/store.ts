import { writable } from "svelte/store";

let uid: number = 0;
let roomId: string = '';
let isRoomOpen: boolean = false;
let uData: string = '';

export const userId = writable(uid);
export const lastRoomCreatedId = writable(roomId);
export const isRoomOpened = writable(isRoomOpen);
export const userData = writable(uData);