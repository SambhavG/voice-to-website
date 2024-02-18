 <script>
 let count = 0;

 function increment() {
 count++;
 }
</script>

<style>
 .component {
 display: flex;
}

 .component > * {
 margin: 0 0.5em;
}

 .button-section button {
 font-size: 1em;
 padding: 0.5em;
}

 .counter-section p {
 font-size: 1.5em;
 margin: 0;
}
</style>

<script>
 export let {}; // remove this line if there are no props

 const increment = () => {
 count++;
 };
</script>

<div class="component">
 <section class="button-section">
 <button on:click={increment}>Increment</button>
 </section>
 <section class="counter-section">
 <p>{count}</p>
 </section>
</div>