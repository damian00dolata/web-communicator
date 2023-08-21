<script lang="ts">
  import MainFooter from "./mainFooter.svelte";
  import MainHeader from "./mainHeader.svelte";
  import RoomList from "./roomList.svelte";
	import ClientList from "./clientList.svelte";
  import Prompt from "./prompt.svelte";
  import { Client } from "../lib/client";
  import { userData } from "../lib/stores/store";

  const client = new Client;
  let nickname: string = '';
  let data = '';
  let usrCreated: boolean = false;

  client.createSocket();
  nickname = client.getClientName();

  userData.subscribe(value => {
    data = value;
  });
</script>

<div class="wrapper">
  {#if data == ''}
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
    width: 100%;
    height: 100%;
    position:fixed;
    top:0;
    left:0;

    font-family: 'Roboto', sans-serif;
    color: #2B2D42;

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