<script lang="ts">
    import { usuario, type ProfessorResponse } from '$lib/api';
    import { onMount } from 'svelte';
    let User = $state<ProfessorResponse | null>(null);
       onMount(async () => {
    User = await usuario.buscar();
  });
    let horas = $derived(new Date().getHours());
  let saudacao = $derived(
    horas < 12 ? 'Bom dia' : horas < 18 ? 'Boa tarde' : 'Boa noite'
  );
</script>
      <h1 class="font-bold text-3xl">Olá, {saudacao} </h1>
      <h1>{User?.nome}</h1>