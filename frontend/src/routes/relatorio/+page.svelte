<script lang="ts">
	import { onMount } from 'svelte';
	import { turmas as turmasApi, chamadas as chamadasApi } from '$lib/api';
	import type { ChamadaItem, TurmaItem } from '$lib/api';

	let datainicio = $state(new Date().toISOString().split('T')[0]);
	let datafim = $state(new Date().toISOString().split('T')[0]);
	let cod = $state('');
	let disciplinaSelecionada = $state('');

	let turmasList = $state<TurmaItem[]>([]);
	let chamadaTurma = $state<ChamadaItem[]>([]);

	onMount(async () => {
		turmasList = await turmasApi.listar();
	});

	$effect(() => {
		if (cod) {
			chamadasApi.listarPorTurma(cod).then((data) => {
				chamadaTurma = data;
			});
			disciplinaSelecionada = '';
		} else {
			chamadaTurma = [];
		}
	});

	let codTurmas = $derived(turmasList.map((t) => t.cod));
	let disciplinas = $derived([...new Set(chamadaTurma.map((c) => c.disciplina))].sort());

	let alunosFiltrados = $derived(
		chamadaTurma.filter((c) => {
			const dataAula = c.data_aula.slice(0, 10);
			const dataOk = dataAula >= datainicio && dataAula <= datafim;
			const discOk =
				disciplinaSelecionada === '' ||
				disciplinaSelecionada === 'todas' ||
				c.disciplina === disciplinaSelecionada;
			return dataOk && discOk;
		})
	);

	let totalAlunos = $derived(alunosFiltrados.length);
	let presentes = $derived(alunosFiltrados.filter((a) => a.presente).length);
	let ausentes = $derived(totalAlunos - presentes);

	let datas = $derived([...new Set(alunosFiltrados.map((c) => c.data_aula.slice(0, 10)))].sort());
	let alunosUnicos = $derived([...new Set(alunosFiltrados.map((c) => c.nome_aluno))]);

	function getPresenca(nomeAluno: string, data: string): boolean | null {
		const registro = chamadaTurma.find(
			(c) => c.nome_aluno === nomeAluno && c.data_aula.slice(0, 10) === data && c.cod_turma === cod
		);
		return registro ? registro.presente : null;
	}

	function getPorcentagem(nomeAluno: string): number {
		const registros = chamadaTurma.filter(
			(c) => c.nome_aluno === nomeAluno && c.cod_turma === cod
		);
		if (!registros.length) return 0;
		return Math.round((registros.filter((c) => c.presente).length / registros.length) * 100);
	}
</script>

<div class="flex flex-col gap-2">
  <div class="flex items-center justify-between">
    <h1 class="text-2xl font-bold">Relatório de Presença</h1>
    <div class="flex gap-3">
      <a
        href="/ExportarPDF"
        class="flex h-10 items-center justify-center gap-2 rounded border border-red-600 bg-white px-4 font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
      >
        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="currentColor">
          <path d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/>
        </svg>
        Exportar PDF
      </a>
      <a
        href="/ExportarEX"
        class="flex h-10 items-center justify-center gap-2 rounded border border-red-600 bg-white px-4 font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
      >
        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="currentColor">
          <path d="M440-120v-480H120v-160q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H440Zm80-80h240v-160H520v160Zm0-240h240v-160H520v160ZM200-680h560v-80H200v80ZM120-80v-80h102q-48-23-77.5-68T115-330q0-79 55.5-134.5T305-520v80q-45 0-77.5 32T195-330q0 39 24 69t61 38v-97h80v240H120Z"/>
        </svg>
        Exportar Excel
      </a>
    </div>
  </div>

  <div class="mb-4 flex flex-col gap-6 rounded-xl border border-gray-200 bg-white p-6 md:flex-row md:items-center">
    <div class="flex min-w-48 flex-col gap-1">
      <label class="text-xs font-medium tracking-wide text-gray-400 uppercase">Turma</label>
      <select bind:value={cod} class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none">
        <option value="">Selecione...</option>
        {#each codTurmas as codigo}
          <option value={codigo}>{codigo}</option>
        {/each}
      </select>
    </div>
    <div class="flex flex-col gap-1">
      <label class="text-xs font-medium tracking-wide text-gray-400 uppercase">Data Início</label>
      <input type="date" bind:value={datainicio} class="rounded-lg border border-gray-200 px-3 py-2 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"/>
    </div>
    <div class="flex flex-col gap-1">
      <label class="text-xs font-medium tracking-wide text-gray-400 uppercase">Data Fim</label>
      <input type="date" bind:value={datafim} class="rounded-lg border border-gray-200 px-3 py-2 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"/>
    </div>
    <div class="flex min-w-48 flex-col gap-1">
      <label class="text-xs font-medium tracking-wide text-gray-400 uppercase">Disciplina</label>
      <select bind:value={disciplinaSelecionada} class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none">
        <option value="">Selecione...</option>
        <option value="todas">Todas</option>
        {#each disciplinas as d}
          <option value={d}>{d}</option>
        {/each}
      </select>
    </div>
  </div>
</div>

<div class="mt-4 overflow-x-auto rounded-xl border border-gray-200 bg-white">
  <table class="w-full">
    <thead>
      <tr class="border-b border-gray-200 bg-gray-50">
        <th class="w-16 px-6 py-4 text-left text-xs font-semibold text-gray-500">Nº</th>
        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500">Nome</th>
        {#each datas as data}
          <th class="px-4 py-4 text-center text-xs font-semibold text-gray-500">
            {data.slice(5).replace('-', '/')}
          </th>
        {/each}
        <th class="px-6 py-4 text-center text-xs font-semibold text-gray-500">% Presença</th>
      </tr>
    </thead>
    <tbody>
      {#each alunosUnicos as nomeAluno, i}
        {@const pct = getPorcentagem(nomeAluno)}
        <tr class="border-b border-gray-100 transition-colors hover:bg-gray-50">
          <td class="px-6 py-4 text-sm font-medium text-red-400">{i + 1}</td>
          <td class="px-6 py-4 text-sm font-medium text-gray-700">{nomeAluno}</td>
          {#each datas as data}
            {@const presente = getPresenca(nomeAluno, data)}
            <td class="px-4 py-4 text-center">
              {#if presente === true}
                <span class="text-lg text-green-500">✓</span>
              {:else if presente === false}
                <span class="text-lg text-red-400">✕</span>
              {:else}
                <span class="text-gray-300">—</span>
              {/if}
            </td>
          {/each}
          <td class="px-6 py-4 text-center">
            <span class="rounded-md px-2 py-1 text-xs font-semibold text-white {pct >= 75 ? 'bg-green-600' : 'bg-red-500'}">
              {pct}%
            </span>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>

  {#if alunosUnicos.length === 0}
    <div class="py-12 text-center text-sm text-gray-400">
      Selecione uma turma para ver o relatório.
    </div>
  {/if}
</div>
