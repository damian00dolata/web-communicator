<script lang="ts">
	import { Room } from "../lib/room";
  import type { Client } from "../lib/client";
	import { RoomList } from "$lib/global/roomList";
  import { roomList } from "../lib/roomListStore";
  export let client: Client;

  let availableRooms: Array<Room> = new Array();
  availableRooms = RoomList.getInstance().getRoomList();
  roomList.subscribe(value => {
    availableRooms = value;
  })
  let roomName: string = '';

  let maxUsers: number;

  function addRoom() {
    var room = new Room(`${roomName}`, 0, maxUsers);
    client.getClientSocket().emit('addRoom', JSON.stringify(room));
  }

  const onKeyPress = (e: { charCode: any; }) => {
    if(e.charCode === 13) addRoom();
  };
</script>

<div class="rooms">
  <div class="roomsHeader">
    Room list
    <input type="text" id="roomName" bind:value={roomName} on:keypress={onKeyPress} placeholder="Room name"/>
    <input type="number" id="maxUsers" bind:value={maxUsers} min=2 max=20 placeholder="Room size"/>
    <button on:click={addRoom}>
      +
    </button>
  </div>
  <div class="roomList">
    {#each availableRooms as room}
      <div class="room">{room.roomName} ({room.currentUsers}/{room.maxUsers})</div>
    {/each}
  </div>
</div>
  
<style>
  .rooms {
    height: 100%;
    width: 100%;
    display: grid;
    grid-area: rooms;
    align-items: center;
    grid-template-rows: 1fr 9fr;
    grid-template-columns: 1fr;
    grid-template-areas:
    "roomsHeader"
    "roomList";
  }

  .roomsHeader {
    display: grid;
    grid-area: roomsHeader;
    
    align-content: center;
    justify-content: center;
    font-size: 18px;
  }

  .roomsHeader button {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
  }

  .roomsHeader button:hover {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.3);
    cursor: pointer;
  }

  .roomList {
    display: grid;
    grid-area: roomList;
    height: 100%;
    align-content: start;
    justify-items: center;
    font-weight: 700;
  }

  .roomList .room {
    display: grid;
    width: 95%;
    height: 25px;
    align-content: center;
    justify-content: center;
    font-size: 14px;
  }

  .roomList div:not(:first-child) {
    /*border-image: linear-gradient(to left, rgba(218,96,20,1), rgba(79,41,24,0.7175)) 1 0 0 0;*/
    border-top: 1px solid;
    border-color: rgba(255, 255, 255, 0.3);
  }
  
</style>