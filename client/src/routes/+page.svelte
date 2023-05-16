<script lang="ts">
  import MainFooter from "./mainFooter.svelte";
  import MainHeader from "./mainHeader.svelte";
  import RoomList from "./roomList.svelte";
	import ClientList from "./clientList.svelte";
  import Prompt from "./prompt.svelte";
  import { Client } from "../lib/client";

  const client = new Client;

  let nickname: string = '';

  let usrCreated: boolean = false;
</script>

<div class="wrapper">
  <div id="stars"></div>
  <div id="stars2"></div>
  <div id="stars3"></div>
  
  {#if nickname == '' || !usrCreated}
    <Prompt client={client} bind:nickname={nickname} bind:usrCreated={usrCreated}/>
  {:else}
    <MainFooter/>
    <MainHeader client={client}/>
    <RoomList client={client}/>
    <ClientList/>
  {/if}
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

  .wrapper {
    font-family: 'Roboto', sans-serif;
    color: white;

    width: 100vw;
    height: 100vh;
    position:fixed;
    padding:0;
    margin:0;

    top:0;
    left:0;

    display: grid;
    align-items: center;
    grid-template-rows: 2fr 18fr 1fr;
    grid-template-columns: 7fr 1fr;
    grid-template-areas:
    "header header"
    "rooms users"
    "footer footer";
  }
</style>