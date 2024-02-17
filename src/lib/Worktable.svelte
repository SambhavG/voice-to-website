<script>
  let countUp = 0;
  const step = 10; // stepped factor
  const increment = () => {
    countUp += step;
    this.increment(); // pass the event to the new count up function
  };
  const decrement = () => {
    if (countUp <= 0) countUp = 0; // reset to zero when count goes below zero
  };
</script>

<button on:click={decrement} class="apple-button">{Math.floor(countUp / step)}</button>
<div on:click={increment}>{Math.floor(countUp / step) > 0 ? "Click me x10!" : "Reset"}</div>

<style>
  button.apple-button {
    background-color: #2f76dc;
    border-radius: 3px;
    color: white;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 18px;
    padding: 10px;
    margin: 10px;
    border: none;
    cursor: pointer;
  }
</style>
