<script lang="ts">
  import { onMount } from 'svelte';
  import { turmas as turmasApi, chamadas as chamadasApi } from '$lib/api';
  import type { ChamadaItem } from '$lib/api';
  import GraficoPizza from '$lib/components/GraficoPizza.svelte';
  import GraficoLinhas from '$lib/components/GraficoLinhas.svelte';
  import GraficoBarras from '$lib/components/GraficoBarras.svelte';

  let codTurmas = $state<string[]>([]);
  let turmaSelecionada = $state('');
  let chamadaTurma = $state<ChamadaItem[]>([]);

  onMount(async () => {
    const ts = await turmasApi.listar();
    codTurmas = ts.map((t) => t.cod);
  });

  $effect(() => {
    if (turmaSelecionada) {
      chamadasApi.listarPorTurma(turmaSelecionada).then((data) => {
        chamadaTurma = data;
      });
    } else {
      chamadaTurma = [];
    }
  });

  let totalAlunos = $derived(chamadaTurma.length);
  let presentes = $derived(chamadaTurma.filter((c) => c.presente === true).length);
  let ausentes = $derived(totalAlunos - presentes);
  let datas = $derived([...new Set(chamadaTurma.map((c) => c.data_aula))].sort());
  let porcentagemPorData = $derived(
    datas.map((data) => {
      const registrosDaData = chamadaTurma.filter((c) => c.data_aula === data);
      if (!registrosDaData.length) return 0;
      const presenteCount = registrosDaData.filter((c) => c.presente).length;
      return Math.round((presenteCount / registrosDaData.length) * 100);
    })
  );
  let AlunosTurma = $derived([...new Set(chamadaTurma.map((c) => c.nome_aluno))]);
  let porcentagemPorAluno = $derived(
    AlunosTurma.map((nome_aluno) => {
      const registros = chamadaTurma.filter((c) => c.nome_aluno === nome_aluno);
      if (!registros.length) return 0;
      return Math.round((registros.filter((c) => c.presente).length / registros.length) * 100);
    })
  );
</script>

<select
  class="rounded-lg w-48 border border-gray-200 bg-white px-3 py-2 text-sm"
  bind:value={turmaSelecionada}
>
  <option value="">Selecione</option>
  {#each codTurmas as t}
    <option value={t}>{t}</option>
  {/each}
</select>

<div class="flex flex-col gap-3 p-4">
  <div class="flex flex-1 flex-row items-center justify-between gap-2">
    <div class="flex h-100 w-full items-center justify-center rounded p-2 shadow">
      <GraficoPizza {presentes} {ausentes} />
    </div>
    <div class="flex h-100 w-full items-center justify-center rounded p-2 shadow">
      <GraficoBarras Alunos={AlunosTurma} Labels={porcentagemPorAluno} />
    </div>
  </div>
  <div>
    <div class="flex h-100 w-full items-center justify-center rounded p-5 shadow">
      <GraficoLinhas presenca={porcentagemPorData} labels={datas} />
    </div>
  </div>
</div>
