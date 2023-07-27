<script lang="ts">
  import type { Client } from "../lib/client";

  export let isRoomOpen: boolean;
  export let roomId: string;
  let message: string;

  export let client: Client

  function closeRoom() {
    client.getClientSocket().emit('leftRoom', roomId);
    isRoomOpen = false;
  }

  function sendMessage() {
    client.getClientSocket().emit('sendMessage', client.getClientName(), message, roomId);
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
</style>