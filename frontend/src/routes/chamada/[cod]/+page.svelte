<script lang="ts">
	import { page } from '$app/state';
	import { nomeTurmaMap, disciplinasMap, chamadas} from '$lib/banco';
	let cod = page.params.cod ?? '3DEVT';

	let nomeTurma         = $derived(nomeTurmaMap[cod] ?? cod);
	let disciplinas       = $derived(disciplinasMap[cod] ?? []);
	let alunosFiltrados   = $derived(chamadas.filter((c) => c.codTurma === cod));
	let totalAlunos       = $derived(alunosFiltrados.length);
	let presentes         = $derived(alunosFiltrados.filter((a) => a.presente).length);
	let ausentes          = $derived(totalAlunos - presentes);

	let dataAula              = $state(new Date().toISOString().split('T')[0]);
	let disciplinaSelecionada = $state('');

function togglePresenca(nomeAluno: string) {
    const idx = chamadas.findIndex((c) => c.nomeAluno === nomeAluno && c.codTurma === cod);
    if (idx !== -1) chamadas[idx].presente = !chamadas[idx].presente;
}
</script>

<!-- Breadcrumb -->
<nav class="flex items-center gap-2 text-sm text-gray-500 mb-6">
	<a href="/" class="text-red-600 hover:underline">Dashboard</a>
	<span>›</span>
	<span class="text-red-600">{cod}</span>
	<span>›</span>
	<span class="text-gray-700">Chamada</span>
</nav>

<!-- Header card -->
<div class="bg-white rounded-xl border border-gray-200 p-6 mb-4 flex flex-col md:flex-row md:items-center gap-6">
	<div class="flex-1">
		<h1 class="text-xl font-bold text-gray-800">{nomeTurma}</h1>
		<p class="text-sm text-gray-400 mt-0.5">{cod}</p>
	</div>

	<div class="flex flex-col gap-1">
		<label class="text-xs text-gray-400 font-medium uppercase tracking-wide">Data</label>
		<input
			type="date"
			bind:value={dataAula}
			class="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
		/>
	</div>

	<div class="flex flex-col gap-1 min-w-48">
		<label class="text-xs text-gray-400 font-medium uppercase tracking-wide">Disciplina</label>
		<select
			bind:value={disciplinaSelecionada}
			class="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
		>
			<option value="">Selecione...</option>
			{#each disciplinas as d}
				<option value={d}>{d}</option>
			{/each}
		</select>
	</div>
</div>

<!-- Resumo -->
<div class="bg-white rounded-xl border border-gray-200 px-6 py-4 mb-4 flex items-center gap-6 text-sm">
	<span class="text-gray-600 font-medium">{totalAlunos} alunos</span>
	<span class="text-green-600 font-semibold">{presentes} presentes</span>
	<span class="text-red-500 font-semibold">{ausentes} ausentes</span>
	<div class="flex-1 bg-gray-100 rounded-full h-2 ml-4">
		<div
			class="bg-green-500 h-2 rounded-full transition-all duration-300"
			style="width: {totalAlunos > 0 ? (presentes / totalAlunos) * 100 : 0}%"
		></div>
	</div>
	<span class="text-gray-400 text-xs">
		{totalAlunos > 0 ? ((presentes / totalAlunos) * 100).toFixed(0) : 0}%
	</span>
</div>

<!-- Tabela -->
<div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
	<table class="w-full">
		<thead>
			<tr class="border-b border-gray-100">
				<th class="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-4 w-24">N.Chamada</th>
				<th class="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-4">Nome do Aluno</th>
				<th class="text-right text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-4 w-32">Presente</th>
			</tr>
		</thead>
		<tbody>
			{#each alunosFiltrados as aluno, i (aluno.nomeAluno)}
				<tr class="border-b border-gray-50 transition-colors {aluno.presente ? 'bg-white' : 'bg-red-50'}">
					<td class="px-6 py-4 text-sm font-medium {aluno.presente ? 'text-gray-400' : 'text-red-300'}">
						{i + 1}
					</td>
					<td class="px-6 py-4 text-sm text-gray-700 font-medium">
						{aluno.nomeAluno}
					</td>
					<td class="px-6 py-4 text-right">
						<button
							onclick={() => togglePresenca(aluno.nomeAluno)}
							aria-label="Marcar presença de {aluno.nomeAluno}"
							class="w-9 h-9 rounded-lg border-2 transition-all duration-150 flex items-center justify-center ml-auto
								{aluno.presente
									? 'bg-green-500 border-green-500 text-white'
									: 'bg-white border-gray-200 hover:border-green-400'}"
						>
							{#if aluno.presente}
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
</div>

<!-- Botão salvar — só aparece quando disciplina selecionada -->
{#if disciplinaSelecionada}
	<div class="mt-6 flex justify-end">
		<a href="/chamada/{cod}/confirmar" class="bg-red-600 hover:bg-red-700 text-white font-medium px-6 py-2.5 rounded-xl transition-colors">
			Salvar Chamada
        </a>
	</div>
{/if}