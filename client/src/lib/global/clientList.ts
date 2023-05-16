import type { Client } from "../client";
import { clientList } from "../clientListStore";

class ClientList {
  private static instance: ClientList;

  private clientList: Array<Client> = new Array();

  private constructor() { }

  public static getInstance(): ClientList { // singleton
    if (!ClientList.instance) {
      ClientList.instance = new ClientList();
    }
    return ClientList.instance;
}

  public getClientList(): Array<Client> {
    return this.clientList;
  }

  public setClientList(currentClients: string): void {
    var jsonData = JSON.parse(currentClients);
    
    for (var i = 0; i < jsonData.length; i++) {
      var r = jsonData[i];
      this.clientList.push(r);
    }
    clientList.set(this.clientList);
  }
}

export { ClientList }