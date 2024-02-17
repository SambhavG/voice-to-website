<script>
  import Worktable from "./lib/Worktable.svelte";
  import userPrompt from "./lib/user-prompt.js";
  import CodeDisplay from "./lib/CodeDisplay.svelte";

  let code = "";
  $: {
    //Set code to the contents of Worktable file whenever Worktable.svelte is updated
    fetch("src/lib/Worktable.txt")
      .then((res) => res.text())
      .then((text) => (code = text));
  }
</script>

<main>
  <div class="header">
    <div class="user-prompt">
      {userPrompt}
    </div>
  </div>
  <div class="contentPanels">
    <CodeDisplay {code} />
    <Worktable />
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
  }
</style>
