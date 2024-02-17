<script>
  import Worktable from "./lib/Worktable.svelte";
  import userPrompt from "./lib/user-prompt.js";
  import CodeDisplay from "./lib/CodeDisplay.svelte";
  import ForceRefresh from "./lib/forceRefresh.svelte";

  let code = "";
  let error = false;
  $: {
    //Set code to the contents of Worktable file whenever Worktable.svelte is updated
    fetch("src/lib/Worktable.txt")
      .then((res) => res.text())
      .then((text) => (code = text));
  }
  $: {
    console.log(error);
  }
</script>

<main>
  <div class="header">
    <div class="user-prompt">
      {userPrompt}
    </div>
  </div>
  <div class="contentPanels">
    <div class="panel">
      <div class="panelHeader">Code</div>
      <CodeDisplay {code} />
    </div>
    <div class="panel">
      <div class="panelHeader">Output</div>
      {#if !error}
        <Worktable
          on:componentError={() => {
            error = true;
            console.log(error);
          }}
        />
      {/if}
    </div>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    height: 100vh;
    width: 100%;
  }
  .header {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 10vh;
  }

  .contentPanels {
    display: grid;
    grid-template-columns: 1fr 1fr;
    width: 100%;
    height: 90vh;
    /* margin between columns: */
    gap: 1rem;
  }

  .panel {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    border: 2px solid black;
    border-radius: 1rem;
    margin: 1rem;
  }

  .panelHeader {
    font:
      1.5rem "Courier New",
      Courier,
      monospace;
    margin: 1rem;
  }
</style>
