import { writable } from "svelte/store";
import type { Client } from "./client";

let currentClients: Array<String> = new Array();
export const clientList = writable(currentClients);