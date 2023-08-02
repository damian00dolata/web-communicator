<script lang="ts">
	import type { Message } from "$lib/message";
	import { get } from "svelte/store";
  import type { Client } from "../lib/client";
  import { isRoomOpened } from "../lib/stores/store";

  export let isRoomOpen: boolean;
  export let roomId: string;
  let message: string;

  export let client: Client

  let messageList: Array<Message> = new Array();

  getMessages(roomId);

  client.getClientSocket().on('returnMessageList', (e: any, f: any) => {
    // userId.set(e);
    // console.log("your id is: " + get(userId));
    //console.log("Messages: " + e);
    //console.log("Room ID: " + f);

    if(f == roomId) {
      var jsonData = JSON.parse(e);
      messageList = [];

      for (var i = 0; i < jsonData.length; i++) {
        var r = jsonData[i];
        messageList.push(r);
      }
      console.log("Messages: " + messageList);
      //console.log("message 1: " + messageList[0].message);
  }
    
  });
  

  function closeRoom() {
    client.getClientSocket().emit('leftRoom', roomId);
    isRoomOpened.set(false);
  }

  function sendMessage() {
    client.getClientSocket().emit('sendMessage', client.getClientName(), message, roomId);
  }

  function getMessages(id: string) {
    client.getClientSocket().emit('getMessages', id);
  }
</script>

<div class="room">
  <button on:click={closeRoom}>
    X
  </button>
  Room {roomId}
  <form on:submit={sendMessage}>
    <input bind:value={message}/>
  </form>
  {#each messageList as mess}
    <div class="message">
      {mess.clientName}: {mess.message} 
    </div>
  {/each}
</div>

<style>
 .room {
   display: inline-block;
   position: fixed;
   width: 50%;
   height: 50%;
   background-color: white;
   color: black;
 }

 .room button {
  width: 40px;
  height: 40px;
 }

 .message {
  display: block;
 }
</style>