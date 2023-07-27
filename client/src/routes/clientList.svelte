<script lang="ts">
	import { ClientList } from "$lib/global/clientList";
  import { clientList } from "../lib/clientListStore";

  let clientRef: any;

  let currentClients: Array<String> = new Array();
  currentClients = ClientList.getInstance().getClientList();
  clientList.subscribe(value => {
    currentClients = value;
  })
</script>

<div class="clients">
  <div class="clientHeader">
    Client list
  </div>
  <div class="clientList" bind:this={clientRef}>
    {#each currentClients as client}
      <div class="client">{client}</div>
    {/each}
  </div>
</div>

<style>
  .clients {
    height: 100%;
    width: 100%;
    display: grid;
    grid-area: users;
    align-content: start;
    justify-content: center;
  }
</style>