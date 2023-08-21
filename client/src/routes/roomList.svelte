<script lang="ts">
  import { Room } from "../lib/room";
  import type { Client } from "../lib/client";
	import { RoomList } from "$lib/global/roomList";
  import { roomList } from "../lib/roomListStore";
  import Chatroom from "./chatroom.svelte";
  import { userId, lastRoomCreatedId, isRoomOpened } from "../lib/stores/store";
  import { get } from 'svelte/store';

  export let client: Client;
  let isRoomOpen: boolean;
  let roomId: string = '';
  let temporary: boolean = false;
  let searchValue: string = '';
  let availableRooms: Array<Room> = new Array();
  let roomName: string = '';
  let maxUsers: number;
  let roomResponse: string = '';

  availableRooms = RoomList.getInstance().getRoomList();
  roomList.subscribe(value => {
    availableRooms = value;
  });

  isRoomOpened.subscribe(value => {
    isRoomOpen = value;
  });

  lastRoomCreatedId.subscribe(value => {
    roomId = get(lastRoomCreatedId);
  })

  client.getClientSocket().emit('generateRoomList');  

  function addRoom() {
    if ((roomName.length >= 5 && roomName.length <= 20) && (maxUsers > 1 && maxUsers <= 20)) {
      let temp: number = (temporary ? 1 : 0);
      var room = new Room('', `${roomName}`, 0, maxUsers, temp);

      client.getClientSocket().emit('addRoom', JSON.stringify(room));
      roomResponse = '';
    } else {
      roomResponse = "Room name must between 5 and 20 characters and max users must be between 2-20.";
    }
  }

  function joinRoom(id: string, name: string) {
    client.getClientSocket().emit('joinedRoom', id, get(userId));
    isRoomOpened.set(true);
    roomId = id;
    roomName = name;
  }

  const onKeyPress = (e: { charCode: any; }) => {
    if(e.charCode === 13) addRoom();
  };
</script>

<div class="rooms">
    {#if isRoomOpen}
      <Chatroom client={client} bind:roomId={roomId} bind:roomName={roomName}/>
    {:else}
    <div class="roomsHeader">
      <div class="inputBox">
        <input type="text" id="roomName" bind:value={roomName} on:keypress={onKeyPress} placeholder="Room name"/>
        <input type="number" id="maxUsers" bind:value={maxUsers} min=2 max=20 placeholder="Room size"/>
        <button on:click={addRoom}>
          <img src="plus-large.svg" alt="+"/>
        </button>
      </div>
      <div class="checkboxBox">
        <input type="checkbox" id="checkbox" bind:checked={temporary}>
        <label for="checkbox">Temporary</label>
      </div>
      <div class="responseBox">
        {roomResponse}
      </div>
      <div class="searchBox">
        <input type="text" id="searchBox" bind:value={searchValue} placeholder="Search"/>
      </div>
    </div>
    <div class="roomList">
      {#each availableRooms as room}
        {#if room.roomName.includes(searchValue) || searchValue == ''}
          <div class="room">{room.roomName} ({room.currentUsers}/{room.maxUsers})
            {#if room.currentUsers == room.maxUsers}
              Room is full!
            {:else}
            <button on:click={() => joinRoom(room.roomId, room.roomName)}>
              <img src="session-join.svg" alt="JOIN"/>
            </button>
            {/if}
          </div>
        {/if}
      {/each}
    </div>
    {/if}
  
</div>
  
<style>
  .rooms {
    height: 80vh;
    width: 100%;

    color: black;

    display: grid;
    grid-area: rooms;
    grid-template-rows: 1fr 9fr;
    grid-template-columns: 1fr;
    grid-template-areas:
        "roomsHeader"
        "roomList";
    overflow-x: auto;
    overflow-y: hidden;
  }

  input {
    height: 30px;
    width: 170px;
    margin: 2px;

    border-radius: 5px;
    border: 1px none #EF233C;
    background-color: #EDF2F4;

    justify-self: center;
    text-align: center;
  }

  .roomsHeader {
    max-height: 180px;
    font-size: 18px;

    display: grid;
    grid-area: roomsHeader;
    grid-template-rows: 1fr 1fr 1fr 1fr;
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
    "inputBox inputBox"
    "checkboxBox checkboxBox"
    "responseBox responseBox"
    "searchBox searchBox";
    align-content: center;
    justify-content: center;
  }

  .roomsHeader button {
    width: 170px;

    background: #EF233C;
    border-radius: 6px;
    border: 1px none rgba(255, 255, 255, 0.3);
    
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .roomsHeader button img {
    width: 20px;
    height: auto;
    margin: 0;
    padding: 0;
    font-weight: 700;

    filter: invert(99%) sepia(1%) saturate(951%) hue-rotate(166deg) brightness(99%) contrast(94%);
  }

  .inputBox {
    display: grid;
    grid-area: inputBox;
    justify-content: center;
  }

  .checkboxBox {
    font-size: 12px;
    
    display: grid;
    grid-area: checkboxBox;
    justify-items: center;
  }

  .checkboxBox input {
    height: 20px;

    accent-color: #EF233C;

    display: inline-block;
  }

  .checkboxBox label {
    display: inline-block;
    text-align: right;
  }

  .responseBox {
    font-size: 12px;

    display: grid;
    grid-area: responseBox;
    justify-content: center;
  }

  .searchBox {
    display: grid;
    grid-area: searchBox;
  }

  .roomList {
    height: 100%;
    font-weight: 700;

    display: grid;
    grid-area: roomList;
    align-content: start;
    justify-items: center;
    overflow-y: auto;
  }

  .roomList .room {
    width: 95%;
    height: 25px;
    font-size: 15px;

    display: inline-block;
    align-content: center;
    justify-content: center;
  }

  .room button {
    padding: 0px;

    background: #EF233C;
    border-radius: 6px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    border: 0px none rgba(255, 255, 255, 0.3);
    color: #EDF2F4;
  }

  .room button img {
    width: 18px;
    height: auto;
    margin: 0;
    padding: 0;
    filter: invert(99%) sepia(1%) saturate(951%) hue-rotate(166deg) brightness(99%) contrast(94%);
  }

  .roomList div:not(:first-child) {
    border-top: 1px solid;
    border-color: rgba(255, 255, 255, 0.3);
  }
</style>