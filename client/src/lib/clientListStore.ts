import { writable } from "svelte/store";

let currentClients: Array<String> = new Array();
export const clientList = writable(currentClients);