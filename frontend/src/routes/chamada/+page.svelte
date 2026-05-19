<script lang="ts">
import { onMount } from 'svelte';
import CardTurma from "$lib/components/CardTurma.svelte";
import { turmas as turmasApi } from '$lib/api';
import type { TurmaItem } from '$lib/api';

let turmasList = $state<TurmaItem[]>([]);

onMount(async () => {
  turmasList = await turmasApi.listar();
});
</script>

<div class="p-4 gap-3 flex flex-col">
  <h1 class="text-xl font-bold text-gray-800">Turmas Disponíveis</h1>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 w-full items-left justify-between">
    {#each turmasList as t}
      <CardTurma
        codTurma={t.cod}
        nomeTurma={t.nome}
        totalAlunos={t.totalAlunos}
      />
    {/each}
  </div>
</div>
