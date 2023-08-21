<script lang="ts">
	import type { Message } from "$lib/message";
	import { get } from "svelte/store";
  import type { Client } from "../lib/client";
  import { isRoomOpened, userId } from "../lib/stores/store";

  export let roomId: string;
  export let roomName: string;
  export let client: Client
  let message: string;
  let messageList: Array<Message> = new Array();
  let messageBox: any;

  getMessages(roomId);

  client.getClientSocket().on('returnMessageList', (e: any, f: any) => {
    if(f == roomId) {
      var jsonData = JSON.parse(e);
      messageList = [];

      for (var i = 0; i < jsonData.length; i++) {
        var r = jsonData[i];
        messageList.push(r);
      }
    }
  });
  
  function closeRoom() {
    client.getClientSocket().emit('leftRoom', roomId, get(userId));
    isRoomOpened.set(false);
  }

  function sendMessage() {
    if (message != '') {
      client.getClientSocket().emit('sendMessage', client.getClientName(), message, roomId);
      message = '';
      messageBox.focus();
    }
  }

  function getMessages(id: string) {
    client.getClientSocket().emit('getMessages', id);
  }

  function init(el: any){
    el.focus();
  }
</script>

<div class="chatroom">
  <div class="roomHeaderButton">
    <button on:click={closeRoom}>
      <img src="cross.svg" alt="X">
    </button>
  </div>
  <div class="roomHeaderName">
    Room {roomName}
  </div>
  <div class="messages">
    {#each messageList as mess}
      <div class="message">
        [{mess.date}] <span>{mess.clientName}</span>: {mess.message} 
      </div>
    {/each}
  </div>
  <div class="messageInput">
    <form on:submit={sendMessage}>
      <input bind:value={message} bind:this={messageBox} use:init/>
    </form>
  </div>
</div>

<style>
 .chatroom {
    width: 100%;
    height: 80vh;

    background-color: white;
    color: black;

    display: grid;
    grid-template-rows: 1fr 16fr 1fr;
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
        "roomHeaderButton roomHeaderName"
        "messages messages"
        "messageInput messageInput";
    overflow-y: auto;
 }

 .roomHeaderButton {
    display: grid;
    grid-area: roomHeaderButton;
    justify-content: start;
 }

 .roomHeaderButton button {
    margin: 5px;
 }

 .roomHeaderButton button img {
    width: 20px;
    height: auto;
    margin: 0;
    padding: 0;

    filter: invert(99%) sepia(1%) saturate(951%) hue-rotate(166deg) brightness(99%) contrast(94%);
    font-weight: 700;
 }

 .chatroom button {
    width: 40px;
    height: 40px;
    padding: 0;

    background: #EF233C;
    border: none;
    border-radius: 6px;

    display: flex;
    justify-content: center;
    align-items: center;
 }

 .roomHeaderName {
    padding: 10px;

    font-size: 20px;
    font-weight: 700;

    display: grid;
    grid-area: roomHeaderName;
    justify-content: end;
    align-content: center;
 }

 .messages {
    max-height: 100vh;

    font-size: 16px;

    display: grid;
    grid-area: messages;
    overflow-y: auto;
    align-content: start;
 }

 .message {
    margin-left: 5px;
    margin-right: 5px;

    display: grid;
    overflow-wrap: anywhere;
    display: inline;
 }

 .message span {
    font-weight: 700;
    color: #EF233C;
 }

 .messageInput {
    width: 100%;

    display: grid;
    grid-area: messageInput;
    align-content: center;
    justify-content: center;
 }

 .messageInput form input {
    height: 30px;
    width: 85vw;
    margin: 2px;
    padding: 10px;

    border-radius: 15px;
    border: 1px solid black;
    background-color: white;

    text-align: left;
    justify-self: center;
 }

 .messageInput form input:focus {
    border: 1px solid #EF233C;
 }
</style>