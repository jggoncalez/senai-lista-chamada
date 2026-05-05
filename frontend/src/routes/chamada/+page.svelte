<script lang="ts">
import CardTurma from "$lib/components/CardTurma.svelte";
import { nomeTurmaMap, disciplinasMap, chamadas} from '$lib/banco';
let codturmas = $derived([...new Set(chamadas.map((c)=> c.codTurma))])
</script>
<div class="p-4 gap-3 flex flex-col">
  <h1 class="text-xl font-bold text-gray-800">Turmas Disponíveis</h1>
<div class="flex flex-row gap-5 w-full items-left justify-between">
  {#each codturmas as t }
  <CardTurma
    codTurma={codturmas[0]}
    nomeTurma={nomeTurmaMap[t]}
    totalAlunos={chamadas.filter((c) => c.codTurma === t ).length}
  />
{/each}
</div>
</div>

