<script lang="ts">
	import GraficoPizza from '$lib/components/GraficoPizza.svelte';
	import GraficoLinhas from '$lib/components/GraficoLinhas.svelte';
	import GraficoBarras from '$lib/components/GraficoBarras.svelte';
	import { onMount } from 'svelte';
	import { turmas as turmasApi, chamadas as chamadasApi } from '$lib/api';
	import type { ChamadaItem } from '$lib/api';
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
<div class="flex flex-col gap-6">

  <!-- Estatísticas Gerais -->
  <div>
    <h2 class="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3">Visão Geral</h2>
    <div class="flex flex-row justify-between gap-4">

      <div class="flex flex-row p-4 bg-white rounded-2xl shadow-sm flex-1 items-center justify-between">
        <div class="flex flex-col gap-1">
          <p class="text-sm text-gray-400">Total de Turmas</p>
          <p class="text-3xl font-bold text-gray-800">{codTurmas.length}</p>
        </div>
        <div class="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
          <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#2563eb">
            <path d="M40-160v-112q0-34 17.5-62.5T104-378q62-31 126-46.5T360-440q66 0 130 15.5T616-378q29 15 46.5 43.5T680-272v112H40Zm720 0v-120q0-44-24.5-84.5T666-434q51 6 96 20.5t84 35.5q36 20 55 44.5t19 53.5v120H760ZM360-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47Zm400-160q0 66-47 113t-113 47q-11 0-28-2.5t-28-5.5q27-32 41.5-71t14.5-81q0-42-14.5-81T544-792q14-5 28-6.5t28-1.5q66 0 113 47t47 113Z"/>
          </svg>
        </div>
      </div>

      <div class="flex flex-row p-4 bg-white rounded-2xl shadow-sm flex-1 items-center justify-between">
        <div class="flex flex-col gap-1">
          <p class="text-sm text-gray-400">Total de Alunos</p>
          <p class="text-3xl font-bold text-gray-800">10</p>
        </div>
        <div class="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
          <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#16a34a">
            <path d="M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-160v-112q0-34 17.5-62.5T224-378q62-31 126-46.5T480-440q66 0 130 15.5T736-378q29 15 46.5 43.5T800-272v112H160Z"/>
          </svg>
        </div>
      </div>

      <div class="flex flex-row p-4 bg-white rounded-2xl shadow-sm flex-1 items-center justify-between">
        <div class="flex flex-col gap-1">
          <p class="text-sm text-gray-400">Frequência Média</p>
          <p class="text-3xl font-bold text-gray-800">87<span class="text-lg text-gray-400">%</span></p>
        </div>
        <div class="flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
          <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#dc2626">
            <path d="M280-280h160v-280H280v280Zm240 0h160v-560H520v560ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Z"/>
          </svg>
        </div>
      </div>

    </div>
  </div>

  <!-- Dashboard por Turma -->
  <div>
    <div class="flex flex-row items-center justify-between mb-3">
      <h2 class="text-xs font-semibold uppercase tracking-widest text-gray-400">Dashboard da Turma</h2>
      <select
        class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm"
        bind:value={turmaSelecionada}
      >
        <option value="">Selecione a turma</option>
        {#each codTurmas as t (t)}
          <option value={t}>{t}</option>
        {/each}
      </select>
    </div>

    {#if turmaSelecionada}
      <!-- Mini stats da turma -->
      <div class="flex flex-row gap-4 mb-4">
        <div class="flex flex-col gap-0.5 bg-white rounded-2xl shadow-sm p-4 flex-1">
          <p class="text-xs text-gray-400">Alunos na turma</p>
          <p class="text-2xl font-bold text-gray-800">{AlunosTurma.length}</p>
        </div>
        <div class="flex flex-col gap-0.5 bg-white rounded-2xl shadow-sm p-4 flex-1">
          <p class="text-xs text-gray-400">Aulas registradas</p>
          <p class="text-2xl font-bold text-gray-800">{datas.length}</p>
        </div>
        <div class="flex flex-col gap-0.5 bg-white rounded-2xl shadow-sm p-4 flex-1">
          <p class="text-xs text-gray-400">Presença geral</p>
          <p class="text-2xl font-bold text-gray-800">
            {totalAlunos ? Math.round((presentes / totalAlunos) * 100) : 0}<span class="text-base text-gray-400">%</span>
          </p>
        </div>
        <div class="flex flex-col gap-0.5 bg-white rounded-2xl shadow-sm p-4 flex-1">
          <p class="text-xs text-gray-400">Ausências totais</p>
          <p class="text-2xl font-bold text-red-500">{ausentes}</p>
        </div>
      </div>

      <!-- Gráficos -->
      <div class="flex flex-row gap-4 mb-4">
        <div class="flex flex-1 flex-col bg-white rounded-2xl shadow-sm p-4">
          <p class="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3">Presença geral</p>
          <div class="flex items-center justify-center">
            <GraficoPizza {presentes} {ausentes} />
          </div>
        </div>
        <div class="flex flex-1 flex-col bg-white rounded-2xl shadow-sm p-4">
          <p class="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3">Frequência por aula</p>
          <div class="flex items-center justify-center">
            <GraficoLinhas presenca={porcentagemPorData} labels={datas} />
          </div>
        </div>
      </div>

      <div class="flex flex-col bg-white rounded-2xl shadow-sm p-4">
        <p class="text-xs font-semibold uppercase tracking-widest text-gray-400 mb-3">Frequência por aluno</p>
        <GraficoBarras Alunos={AlunosTurma} Labels={porcentagemPorAluno} />
      </div>

    {:else}
      <div class="flex flex-col items-center justify-center bg-white rounded-2xl shadow-sm p-12 text-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#d1d5db">
          <path d="M480-280q17 0 28.5-11.5T520-320q0-17-11.5-28.5T480-360q-17 0-28.5 11.5T440-320q0 17 11.5 28.5T480-280Zm-40-160h80v-240h-80v240Zm40 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Z"/>
        </svg>
        <p class="text-sm text-gray-400">Selecione uma turma para ver o dashboard</p>
      </div>
    {/if}
  </div>

</div>