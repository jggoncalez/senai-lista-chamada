<script lang="ts">
  import { page } from '$app/state';
  import { onMount } from 'svelte';
  import { alunos as alunosApi, chamadas as chamadasApi,} from '$lib/api';
  import type { ChamadaItem } from '$lib/api';
  import type { ChamadaCreate } from '$lib/api';
  import { goto } from '$app/navigation';

  let cod = page.params.cod ?? '3DEVT';
  let dataAula = $state(new Date().toISOString().split('T')[0]);
  let disciplinaSelecionada = $state('');

  interface Aluno { id: number; nome: string; turma: string; cod_turma: string; chamada: number | null; }
  let listaAlunos = $state<Aluno[]>([]) ;
  let carregando = $state(true);
  let erro = $state('');
  let presencaMap = $state<Record<string, boolean>>({});

  let nomeTurma = $derived(listaAlunos[0]?.turma ?? cod);
  let chamadaTurma = $state<ChamadaItem[]>([]);
    $effect(() => {
    if (cod) {
      chamadasApi.listarPorTurma(cod).then((data) => {
        chamadaTurma = data;
      });
    } else {
      chamadaTurma = [];
    }
  });
   let disciplinas = $derived([...new Set(chamadaTurma.map((c) => c.disciplina))].sort());

  let totalAlunos = $derived(listaAlunos.length);
  let presentes = $derived(Object.values(presencaMap).filter(Boolean).length);
  let ausentes = $derived(totalAlunos - presentes);

  onMount(async () => {
    try {
      listaAlunos = await alunosApi.porTurma(cod);
      presencaMap = Object.fromEntries(listaAlunos.map((a) => [a.nome, true]));
    } catch {
      erro = 'Erro ao carregar alunos. Backend rodando?';
    } finally {
      carregando = false;
    }
  });


  function togglePresenca(nomeAluno: string) {
    presencaMap[nomeAluno] = !presencaMap[nomeAluno];
  }

function irParaConfirmar() {
  goto(`/chamada/${cod}/confirmar`, {
    state: {
      // Use $state.snapshot() diretamente aqui
      nomeTurma: $state.snapshot(nomeTurma),
      dataAula: $state.snapshot(dataAula),
      disciplinaSelecionada: $state.snapshot(disciplinaSelecionada),
      presencaMap: $state.snapshot(presencaMap),
      listaAlunos: $state.snapshot(listaAlunos)
    }
  });
}
</script>

<!-- Breadcrumb -->
<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500">
	<a href="/" class="text-red-600 hover:underline">Dashboard</a>
	<span>›</span>
	<span class="text-red-600">{cod}</span>
	<span>›</span>
	<span class="text-gray-700">Chamada</span>
</nav>

<!-- Header card -->
<div
	class="mb-4 flex flex-col gap-6 rounded-xl border border-gray-200 bg-white p-6 md:flex-row md:items-center"
>
	<div class="flex-1">
		<h1 class="text-xl font-bold text-gray-800">{nomeTurma}</h1>
		<p class="mt-0.5 text-sm text-gray-400">{cod}</p>
	</div>

	<div class="flex flex-col gap-1">
		<label class="text-xs font-medium tracking-wide text-gray-400 uppercase">Data</label>
		<input
			type="date"
			bind:value={dataAula}
			class="rounded-lg border border-gray-200 px-3 py-2 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"
		/>
	</div>

	<div class="flex min-w-48 flex-col gap-1">
		<label class="text-xs font-medium tracking-wide text-gray-400 uppercase">Disciplina</label>
		<select
			bind:value={disciplinaSelecionada}
			class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"
		>
			<option value="">Selecione...</option>
			{#each disciplinas as d}
				<option value={d}>{d}</option>
			{/each}
		</select>
	</div>
</div>

<!-- Resumo -->
<div
	class="mb-4 flex items-center gap-6 rounded-xl border border-gray-200 bg-white px-6 py-4 text-sm"
>
	<span class="font-medium text-gray-600">{totalAlunos} alunos</span>
	<span class="font-semibold text-green-600">{presentes} presentes</span>
	<span class="font-semibold text-red-500">{ausentes} ausentes</span>
	<div class="ml-4 h-2 flex-1 rounded-full bg-gray-100">
		<div
			class="h-2 rounded-full bg-green-500 transition-all duration-300"
			style="width: {totalAlunos > 0 ? (presentes / totalAlunos) * 100 : 0}%"
		></div>
	</div>
	<span class="text-xs text-gray-400">
		{totalAlunos > 0 ? ((presentes / totalAlunos) * 100).toFixed(0) : 0}%
	</span>
</div>

<!-- Tabela -->
<div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
  {#if carregando}
    <div class="py-12 text-center text-sm text-gray-400">Carregando alunos...</div>
  {:else if erro}
    <div class="py-12 text-center text-sm text-red-500">{erro}</div>
  {:else}
    <table class="w-full">
      <thead>
        <tr class="border-b border-gray-100">
          <th class="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-4 w-24">N.Chamada</th>
          <th class="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-4">Nome do Aluno</th>
          <th class="text-right text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-4 w-32">Presente</th>
        </tr>
      </thead>
      <tbody>
        {#each listaAlunos as aluno, i (aluno.id)}
          <tr class="border-b border-gray-50 transition-colors {presencaMap[aluno.nome] ? 'bg-white' : 'bg-red-50'}">
            <td class="px-6 py-4 text-sm font-medium {presencaMap[aluno.nome] ? 'text-gray-400' : 'text-red-300'}">
              {aluno.chamada ?? i + 1}
            </td>
            <td class="px-6 py-4 text-sm text-gray-700 font-medium">{aluno.nome}</td>
            <td class="px-6 py-4 text-right">
              <button
                onclick={() => togglePresenca(aluno.nome)}
                class="w-9 h-9 rounded-lg border-2 transition-all duration-150 flex items-center justify-center ml-auto
                  {presencaMap[aluno.nome] ? 'bg-green-500 border-green-500 text-white' : 'bg-white border-gray-200 hover:border-green-400'}"
              >
                {#if presencaMap[aluno.nome]}
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 00-1.414 0L8 12.586 4.707 9.293a1 1 0 00-1.414 1.414l4 4a1 1 0 001.414 0l8-8a1 1 0 000-1.414z" clip-rule="evenodd"/>
                  </svg>
                {/if}
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>

{#if disciplinaSelecionada && !carregando && !erro}
  <div class="mt-6 flex justify-end">
    <button
      onclick={irParaConfirmar}
      class="bg-red-600 hover:bg-red-700 text-white font-medium px-6 py-2.5 rounded-xl transition-colors"
    >
      Salvar Chamada
    </button>
  </div>
{/if}


