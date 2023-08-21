<script lang="ts">
  import type { Client } from "../lib/client";
  import { userData } from "../lib/stores/store";

  export let client: Client;

  function logout() {
    userData.set('');
    client.getClientSocket().disconnect();
    client.setClientName('');
    client.createSocket();
  }
</script>

<div class="header">
  <div class="headerBox">
    <h5>Web Communicator</h5>
  </div>
  <div class="userBox">
    <h6>Hello, {client.getClientName()}!</h6>
    <button on:click={() => logout()}>Logout</button>
  </div>
</div>

<style>
  .header {
    height: 100%;
    width: 100%;

    font-size: 30px;

    display: grid;
    grid-area: header;
    grid-template-rows: 1fr;
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
    "headerBox userBox";
    align-content: center;
  }

  .header h5 {
    padding: 25px;
    font-size: 70px;
    font-weight: 600;

    background-image: linear-gradient(45deg, #EF233C, #553c9a);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;

    display: grid;
    align-self: start;
  }

  .header button {
    height: 40px;
    padding: 3px;
    font-size: 16px;
    font-weight: 700;

    color: #EF233C;
    background-color: white;
    border: 2px solid #EF233C;
    transition: 0.1s;

    display: flex;
    justify-content: center;
    align-items: center;
  }

  .header button:hover {
    color: white;
    background-color: #EF233C;
    border: 2px solid #EF233C;
  }

  .headerBox {
    display: grid;
    grid-area: headerBox;
    justify-items: start;
    align-items: center;
  }

  .userBox {
    padding: 40px;
    
    display: grid;
    grid-area: userBox;
    justify-items: end;
    align-items: center;
  }
</style>