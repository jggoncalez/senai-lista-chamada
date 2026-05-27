<script lang="ts">
  import { page } from '$app/state';
  import { onMount } from 'svelte';
  import { 
    alunos as alunosApi, 
    turmaDisciplinas, 
    chamadas as chamadasApi, 
    cursos as cursosApi,
    usuario as usuarioApi,   // ← adicione
  } from '$lib/api';
  import type { TurmaDisciplinaItem, CursoItem } from '$lib/api';
  import { goto } from '$app/navigation';

  let cod = page.params.cod ?? '';
  let dataAula = $state(new Date().toISOString().split('T')[0]);
  let disciplinaSelecionada = $state<number | null>(null);
  let professorId = $state<number | null>(null);   // ← adicione

  interface Aluno { 
    id: number; 
    nome: string; 
    turma: string; 
    cod_turma: string; 
    chamada: number | null; 
  }
  let listaAlunos = $state<Aluno[]>([]);
  let carregando = $state(true);
  let erro = $state('');
  let presencaMap = $state<Record<number, boolean>>({});
  let tdList = $state<TurmaDisciplinaItem[]>([]);
  let cursosMap = $state<Record<number, string>>({});

	let nomeTurma = $derived(listaAlunos[0]?.turma ?? cod);
	let totalAlunos = $derived(listaAlunos.length);
	let presentes = $derived(Object.values(presencaMap).filter(Boolean).length);
	let ausentes = $derived(totalAlunos - presentes);

	// Disciplinas disponíveis com nome do curso
	let disciplinasDisponiveis = $derived(
		tdList.map((td) => ({
			td_id: td.id,
			curso_id: td.curso_id,
			nome: cursosMap[td.curso_id] ?? `Disciplina ${td.curso_id}`
		}))
	);

onMount(async () => {
  try {
    const [alunosData, cursosData] = await Promise.all([
      alunosApi.porTurma(cod),
      cursosApi.listar(),
    ]);

    listaAlunos = alunosData;
    presencaMap = Object.fromEntries(alunosData.map((a: Aluno) => [a.id, true]));
    cursosMap = Object.fromEntries(cursosData.map((c: CursoItem) => [c.id, c.nome]));

    try {
      const user = await usuarioApi.buscar();
      professorId = user.id;
      console.log('professorId carregado:', professorId);
    } catch {
      console.error('Falha ao buscar professor');
    }

    // Busca turma pelo cod_turma e filtra turma-disciplinas corretamente
    const turmasResp = await fetch(`http://localhost:8000/turmas`).then(r => r.json());
    const turmaObj = turmasResp.find((t: { id: number; cod_turma: string }) => t.cod_turma === cod);

    if (turmaObj) {
      tdList = await fetch(`http://localhost:8000/turma-disciplinas?turma_id=${turmaObj.id}&apenas_ativas=true`)
        .then(r => r.json()) as TurmaDisciplinaItem[];
    }

  } catch {
    erro = 'Erro ao carregar dados. Backend rodando?';
  } finally {
    carregando = false;
  }
});

	function togglePresenca(alunoId: number) {
		presencaMap[alunoId] = !presencaMap[alunoId];
	}

	async function irParaConfirmar() {
  if (!disciplinaSelecionada) return;
  if (!professorId) {
    erro = 'Professor não carregado. Recarregue a página.';
    return;
  }

  goto(`/chamada/${cod}/confirmar`, {
    state: {
      nomeTurma: $state.snapshot(nomeTurma),
      dataAula: $state.snapshot(dataAula),
      disciplinaId: disciplinaSelecionada,
      disciplinaNome: disciplinasDisponiveis.find(d => d.td_id === disciplinaSelecionada)?.nome ?? '',
      presencaMap: $state.snapshot(presencaMap),
      listaAlunos: $state.snapshot(listaAlunos),
      professorId: $state.snapshot(professorId),
    },
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
			class="rounded-lg border border-gray-200 px-3 py-2 text-sm focus:ring-2 focus:ring-red-400 focus:outline-none"
		/>
	</div>

	<div class="flex min-w-56 flex-col gap-1">
		<label class="text-xs font-medium tracking-wide text-gray-400 uppercase">Disciplina</label>
		<select
			bind:value={disciplinaSelecionada}
			class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm focus:ring-2 focus:ring-red-400 focus:outline-none"
		>
			<option value={null}>Selecione...</option>
			{#each disciplinasDisponiveis as d}
				<option value={d.td_id}>{d.nome}</option>
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
<div class="overflow-hidden rounded-xl border border-gray-200 bg-white">
	{#if carregando}
		<div class="py-12 text-center text-sm text-gray-400">Carregando alunos...</div>
	{:else if erro}
		<div class="py-12 text-center text-sm text-red-500">{erro}</div>
	{:else}
		<table class="w-full">
			<thead>
				<tr class="border-b border-gray-100">
					<th
						class="w-24 px-6 py-4 text-left text-xs font-semibold tracking-wide text-gray-400 uppercase"
						>N.Chamada</th
					>
					<th
						class="px-6 py-4 text-left text-xs font-semibold tracking-wide text-gray-400 uppercase"
						>Nome do Aluno</th
					>
					<th
						class="w-32 px-6 py-4 text-right text-xs font-semibold tracking-wide text-gray-400 uppercase"
						>Presente</th
					>
				</tr>
			</thead>
			<tbody>
				{#each listaAlunos as aluno, i (aluno.id)}
					<tr
						class="border-b border-gray-50 transition-colors {presencaMap[aluno.id]
							? 'bg-white'
							: 'bg-red-50'}"
					>
						<td
							class="px-6 py-4 text-sm font-medium {presencaMap[aluno.id]
								? 'text-gray-400'
								: 'text-red-300'}"
						>
							{aluno.chamada ?? i + 1}
						</td>
						<td class="px-6 py-4 text-sm font-medium text-gray-700">{aluno.nome}</td>
						<td class="px-6 py-4 text-right">
							<button
								onclick={() => togglePresenca(aluno.id)}
								class="ml-auto flex h-9 w-9 items-center justify-center rounded-lg border-2 transition-all duration-150
                  {presencaMap[aluno.id]
									? 'border-green-500 bg-green-500 text-white'
									: 'border-gray-200 bg-white hover:border-green-400'}"
							>
								{#if presencaMap[aluno.id]}
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-5 w-5"
										viewBox="0 0 20 20"
										fill="currentColor"
									>
										<path
											fill-rule="evenodd"
											d="M16.707 5.293a1 1 0 00-1.414 0L8 12.586 4.707 9.293a1 1 0 00-1.414 1.414l4 4a1 1 0 001.414 0l8-8a1 1 0 000-1.414z"
											clip-rule="evenodd"
										/>
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
			class="rounded-xl bg-red-600 px-6 py-2.5 font-medium text-white transition-colors hover:bg-red-700"
		>
			Salvar Chamada
		</button>
	</div>
{/if}
