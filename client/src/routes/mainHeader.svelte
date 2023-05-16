<script lang="ts">
  import type { Client } from "../lib/client";
// 	import { afterUpdate } from "svelte";

//   afterUpdate(() => {
// 	if (autoscroll) div.scrollTo(0, div.scrollHeight);
// });
  export let client: Client;
</script>

<div class="header">
  <h5>Web Communicator</h5>
  <h6>Hello, {client.getClientName()}!</h6>
</div>

<style>
  .header {
    height: 100%;
    width: 100%;
    display: grid;
    grid-area: header;

    align-content: center;
    justify-content: center;
    justify-items: center;
    font-size: 30px;
  }
</style>