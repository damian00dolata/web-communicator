<script lang="ts">
 	import type { Client } from "../lib/client";
  import { fade } from 'svelte/transition';
  //import { userId } from '../lib/stores/store';
  export let client: Client;

  export let nickname: string = '';

  export let usrCreated: boolean = false;

  function createUser() {
    client.setClientName(nickname);
    client.createSocket();
    //userId.set(client.getClientSocket());
    usrCreated = true;
    //client.getClientSocket().emit('generateUserId');
    client.getClientSocket().emit('addClient', client.getClientName());
    console.log('Your name is ' + client.getClientName() + "\nYour token is: " + client.getClientSocket());
  }

  const onKeyPress = (e: { charCode: any; }) => {
    if(e.charCode === 13) createUser();
  };
</script>

<div class="prompt" transition:fade>
  <div class="welcomeBox">
    <h2>Enter your nickname</h2>
    <input type="text" id="nickname" bind:value={nickname} on:keypress={onKeyPress}/> <!-- bind:value={$user.name} -->
    <button on:click={createUser}>Enter</button> <!--  -->
  </div>
</div>

<style>
  .prompt {
    display: grid;
    position: fixed;
    align-items: center;
    width: 100vw;
    height: 100vh;
    backdrop-filter: blur(10px);
  }

  .welcomeBox {
    display: grid;
    width: 100%;
    height: 100%;
    justify-content: center;
    align-content: center;
    justify-items: center;
    color: white;
  }

  .welcomeBox button {
    width: 50%;
  }
</style>