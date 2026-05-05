<script lang="ts">
	import { chamadas } from '$lib/banco';
	import GraficoPizza from '$lib/components/GraficoPizza.svelte';
	import GraficoLinhas from '$lib/components/GraficoLinhas.svelte';
	import GraficoBarras from '$lib/components/GraficoBarras.svelte';
	let codTurmas = $derived([...new Set(chamadas.map((c) => c.codTurma))]);
	let turmaSelecionada = $state('');
	let turmas = $derived(chamadas.filter((c) => c.codTurma === turmaSelecionada));
	let totalAlunos = $derived(turmas.length);
	let presentes = $derived(turmas.filter((c) => c.presente === true).length);
	let ausentes = $derived(totalAlunos - presentes);
	let datas = $derived([...new Set(chamadas.map((c) => c.dataAula))].sort());
	let porcentagemPorData = $derived(
		datas.map((data) => {
			const registrosDaData = chamadas.filter(
				(c) => c.codTurma === turmaSelecionada && c.dataAula === data
			);
			if (!registrosDaData.length) return 0;
			const presenteCount = registrosDaData.filter((c) => c.presente).length;
			return Math.round((presenteCount / registrosDaData.length) * 100);
		})
	);
	let AlunosTurma = $derived(turmas.map((c) => c.nomeAluno));
	let porcentagemPorAluno = $derived(
		AlunosTurma.map((nomeAluno) => {
			const registros = chamadas.filter(
				(c) => c.nomeAluno === nomeAluno && c.codTurma === turmaSelecionada
			);
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
	<div class="flex flex-1  flex-row items-center justify-between gap-2">
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
