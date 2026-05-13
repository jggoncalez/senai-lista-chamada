<script lang="ts">
  import Saudacao from '$lib/components/saudacao.svelte';
  import AcessoRapido from '$lib/components/acessoRapido.svelte';
  import Dashboard from '$lib/components/dashboard.svelte';
</script>
<div class="flex flex-col gap-10 p-4">
  <div class="flex flex-col p-4 bg-white rounded-2xl shadow-sm">
      <Saudacao />
  </div>
    <AcessoRapido />
  <div class="flex flex-col p-4 bg-white rounded-2xl shadow-sm gap-7">
    <Dashboard />
  </div>
</div>
