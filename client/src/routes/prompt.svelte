<script lang="ts">
 	import type { Client } from "../lib/client";
  import { fade } from 'svelte/transition';
  import { userData } from "../lib/stores/store";

  export let client: Client;
  export let nickname: string = '';
  export let usrCreated: boolean = false;
  let registerNickname: string = '';
  let registerEmail: string = '';
  let registerPassword: string = '';
  let loginNickname: string = '';
  let loginPassword: string = '';
	let currentView = 0;
  let ul: HTMLElement | null;

  function clearFormResponse() {
    while (ul?.firstChild) {
      ul.removeChild(ul.firstChild);
      }
  }

  function addFormResponse(response: string) {
    let li = document.createElement("li");
    li.appendChild(document.createTextNode(response));
    ul?.appendChild(li);
  }

  async function createUser() {
    let nicknameRegex = /^(?=.{5,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$/;
    let emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    let passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    let nicknameResult = nicknameRegex.test(registerNickname);
    let emailResult = emailRegex.test(registerEmail);
    let passwordResult = passwordRegex.test(registerPassword);
    ul = document.getElementById("formResponse");
    
    if(nicknameResult && emailResult && passwordResult) {
      const response = await fetch("http://localhost:8000/user/register", {
        method: "POST",
        body: JSON.stringify({
          username: registerNickname,
          email: registerEmail,
          password: registerPassword
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      });

      if(response.ok) {
        const data = await response.json();
        userData.set(JSON.stringify(data));
        usrCreated = true;
        nickname = registerNickname;
        client.setClientName(nickname);
        client.getClientSocket().emit('addClient', client.getClientName());
      } else {
        let responseText = await response.json();
        clearFormResponse();
        addFormResponse("[" + response.status + "] " + response.statusText + ": " + responseText.message);
      }
    } else {
      clearFormResponse();
      if (!nicknameResult) {
        addFormResponse("Nickname must be 5-20 characters long, contain only alphanumeric characters, underscores and dots, that can't be at the beginning or the end of a nickname.");
      }
      if (!emailResult) {
        addFormResponse("Email must have a @ and a dot, domain can't be longer than 4 characters.");
      }
      if (!passwordResult) {
        addFormResponse("Password must be 8 characters or longer and have at least one alphanumeric character and a number.");
      }
    }
  }

  async function authUser() {
    ul = document.getElementById("formResponse");

    const response = await fetch("http://localhost:8000/user/login", {
      method: "POST",
      body: JSON.stringify({
        username: loginNickname,
        password: loginPassword
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });

    if(response.ok) {
      const data = await response.json();
      userData.set(JSON.stringify(data));
      usrCreated = true;
      nickname = loginNickname;
      client.setClientName(nickname);
      client.getClientSocket().emit('addClient', client.getClientName());
    } else {
      let responseText = await response.json();
      clearFormResponse()
      addFormResponse("[" + response.status + "] " + response.statusText + ": " + responseText.message);
    }
  }

  function buttonSwap() {
    currentView = currentView == 0 ? 1 : 0;
  }

  const onKeyPressRegister = (e: { charCode: any; }) => {
    if(e.charCode === 13) createUser();
  };

  const onKeyPressLogin = (e: { charCode: any; }) => {
    if(e.charCode === 13) authUser();
  };
</script>

<div class="prompt" transition:fade>
  <div class="welcomeBox">
    <div class="buttonSwapBox">
      <div class="buttonSwapLeft">
        <button on:click={buttonSwap} class:active="{currentView === 1}">REGISTER</button>
      </div>
      <div class="buttonSwapRight">
        <button on:click={buttonSwap} class:active="{currentView === 0}">LOGIN</button>
      </div>
    </div>
    {#if currentView == 0}
      <div class="formBox">
        <div class="inputBox">
          <input type="text" id="nickname" bind:value={loginNickname} placeholder="Nickname" on:keypress={onKeyPressLogin}/>
          <input type="password" id="password" bind:value={loginPassword} placeholder="Password" on:keypress={onKeyPressLogin}/>
        </div>
        <div class="inputButtonBox">
          <button on:click={authUser}>Login</button>
        </div>
      </div>
    {:else}
      <div class="formBox">
        <div class="inputBox">
          <input type="text" id="nickname" bind:value={registerNickname} placeholder="Nickname" on:keypress={onKeyPressRegister}/>
          <input type="text" id="email" bind:value={registerEmail} placeholder="Email" on:keypress={onKeyPressRegister}/>
          <input type="password" id="password" bind:value={registerPassword} placeholder="Password" on:keypress={onKeyPressRegister}/>
        </div>
        <div class="inputButtonBox">
          <button on:click={createUser}>Register</button>
        </div>
      </div>
    {/if}
    <div class=formResponseBox>
      <ul id="formResponse"></ul>
    </div>
  </div>
</div>

<style>
  .prompt {
    width: 100%;
    height: 100%;

    backdrop-filter: blur(10px);

    display: grid;
    position: fixed;
    align-items: center;
  }

  .welcomeBox {
    width: 30%;
    height: 40%;
    
    display: grid;
    justify-self: center;
    justify-content: center;
    justify-items: center;
    align-self: center;
    align-content: center;
    align-items: center;
    grid-template-rows: 1fr 5fr 3fr;
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
    "buttonSwap buttonSwap"
    "form form"
    "response response";
  }

  input {
    height: 30px;
    margin: 2px;

    border-radius: 5px;
    border: 1px none #EF233C;
    background-color: #EDF2F4;
    
    justify-self: center;
    text-align: center;
  }

  .welcomeBox button {
    width: 100%;
    height: 40px;
    padding: 5px;
    font-size: 16px;
    font-weight: 700;

    color: #EF233C;
    background-color: white;
    border: 2px solid #EF233C;
    
    align-self: end;
    transition: 0.1s;
  }

  .welcomeBox button:focus{
    outline: none;
  }

  .buttonSwapLeft > .active, .buttonSwapRight > .active {
    color: white;
    background-color: #EF233C;
    border: 2px solid #EF233C;
  }

  .inputButtonBox button:hover {
    background-color: #EF233C;
    border: 2px solid #EF233C;
    color: white;
  }

  .buttonSwapBox {
    width: 100%;
    height: 100%;

    display: grid;
    grid-area: buttonSwap;
    grid-template-rows: 1fr;
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
    "buttonLeft buttonRight";
  }

  .buttonSwapLeft {
    display: grid;
    grid-area: buttonLeft;
    justify-items: end;
  }

  .buttonSwapRight {
    display: grid;
    grid-area: buttonRight;
    justify-items: start;
  }

  .formBox {
    padding: 5px;

    display: grid;
    grid-area: form;
    grid-template-rows: 3fr 1fr;
    grid-template-columns: 1fr;
    grid-template-areas:
    "formInput"
    "formButton";
    justify-items: center;
  }

  .inputBox {
    display: grid;
    grid-area: formInput;
  }

  .inputButtonBox {
    display: grid;
    grid-area: formButton;
  }

  .formResponseBox {
    font-size: 12px;
    display: grid;
    grid-area: response;
  }

  ul {
    list-style-type: none;
  }
</style>