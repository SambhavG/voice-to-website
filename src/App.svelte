<script>
  import Worktable from "./lib/Worktable.svelte";
  import userPrompt from "./lib/user-prompt.js";
</script>

<main>
  <div class="user-prompt">
    {userPrompt}
  </div>
  <Worktable />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>
