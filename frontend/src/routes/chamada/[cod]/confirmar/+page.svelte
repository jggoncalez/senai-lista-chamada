<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import CardConfirm from '$lib/components/CardConfirm.svelte';
	import { chamadas as chamadasApi, sessoes as sessoesApi } from '$lib/api';

	/** @type {any} */
	const pageState = page.state;
	let nomeTurma = $derived(pageState.nomeTurma ?? 'Não informada');
	let dataAula = $derived(pageState.dataAula ?? '');
	let disciplinaId = $derived(pageState.disciplinaId ?? null); // turma_disciplina_id
	let disciplinaNome = $derived(pageState.disciplinaNome ?? '');
	let presencaMap = $derived(pageState.presencaMap ?? {}); // { aluno_id: boolean }
	let listaAlunos = $derived(pageState.listaAlunos ?? []);
	let professorId = $derived(pageState.professorId ?? null);
	let totalAlunos = $derived(listaAlunos.length);
	let totalPresentes = $derived(Object.values(presencaMap).filter((p) => p === true).length);

	let cod = page.params.cod ?? '';
	let salvando = $state(false);
	let erroSalvar = $state('');

	async function salvarChamada() {
		if (!disciplinaId) {
			erroSalvar = 'Disciplina não informada.';
			return;
		}
		try {
			salvando = true;
			erroSalvar = '';

			// 1. Cria ou busca a sessão do dia
			const sessao = await sessoesApi.criarOuBuscar({
				turma_disciplina_id: disciplinaId,
				professor_id: professorId, // ← adicione esta linha
				data_aula: dataAula
			});

			// 2. Monta lista de presenças usando ID numérico do aluno
			const presencas = listaAlunos.map((aluno: any) => ({
				aluno_id: aluno.id,
				presente: presencaMap[aluno.id] ?? true
			}));

			// 3. Salva lote
			await chamadasApi.salvarLote(sessao.id, presencas);

			goto('/');
		} catch (e: any) {
			erroSalvar = e.message ?? 'Erro ao salvar chamada.';
		} finally {
			salvando = false;
		}
	}
</script>

<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500">
	<a href="/" class="text-red-600 hover:underline">Dashboard</a>
	<span>›</span>
	<span class="text-gray-700">{cod}</span>
	<span>›</span>
	<span class="text-gray-700">Chamada</span>
	<span>›</span>
	<span class="text-red-600">Confirmar</span>
</nav>

<div class="flex w-full flex-1 flex-col items-center justify-center gap-3 p-5">
	<h1 class="text-2xl font-bold">Confirmar Chamada</h1>

	<CardConfirm
		{nomeTurma}
		data={dataAula}
		diciplina={disciplinaNome}
		professor="Professor"
		presentes={totalPresentes}
		{totalAlunos}
	/>

	{#if erroSalvar}
		<div
			class="w-full max-w-2xl rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700"
		>
			{erroSalvar}
		</div>
	{/if}

	<div class="flex w-full max-w-2xl items-center justify-between">
		<a
			href="/chamada/{cod}"
			class="flex items-center gap-2 text-sm text-gray-500 transition-colors hover:text-gray-800"
		>
			‹ Voltar e Corrigir
		</a>
		<button
			onclick={salvarChamada}
			disabled={salvando}
			class="rounded-xl bg-red-600 px-6 py-2.5 font-medium text-white transition-colors hover:bg-red-700 disabled:bg-gray-300"
		>
			{salvando ? 'Salvando...' : 'Confirmar Chamada'}
		</button>
	</div>
</div>
