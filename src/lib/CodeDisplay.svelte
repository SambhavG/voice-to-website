<script>
  let x = 979;
  import { HighlightAuto } from "svelte-highlight";
  import githubDark from "svelte-highlight/styles/github-dark";

  export let code = `console.log('Hello world')`;
</script>

<svelte:head>
  {@html githubDark}
</svelte:head>

<div class="code">
  <HighlightAuto {code} />
  <div class="x">{x}</div>
</div>

<style>
  .code {
    white-space: pre-wrap;
    display: block;
    text-align: left;
    font-family: "Courier New", Courier, monospace;
  }
  .x {
    opacity: 0;
  }
</style>
