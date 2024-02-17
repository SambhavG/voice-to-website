<script>
  import Prism from "prismjs";
  import "prism-svelte";
  import "prismjs/themes/prism-coy.css";

  export let code = `console.log('Hello world')`;

  // Get code from Worktable.txt
  fetch("src/lib/Worktable.txt")
    .then((res) => res.text())
    .then((text) => (code = text));
</script>

<div class="code">
  {@html Prism.highlight(code, Prism.languages.svelte, "svelte")}
</div>

<!-- <svelte:head>
  <link href="prismjs/themes/prism-coy.css" rel="stylesheet" />
</svelte:head> -->

<style>
  .code {
    white-space: pre-wrap;
    display: block;
    /* align left */
    text-align: left;
    font-family: "Courier New", Courier, monospace;
  }
</style>
