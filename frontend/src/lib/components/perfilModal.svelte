<script>
    let {status, onclose} = $props()
</script>

{#if status}
<div class="fixed inset-0  z-50 flex items-center justify-center bg-black/50 rounded-lg shadow-xl p-6 flex flex-col">
<p>modau</p>
<button onclick={onclose}> fechar</button>
</div>

{/if}