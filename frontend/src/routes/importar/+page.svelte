<script lang="ts">
	import { parseExcelFile, validateRow } from '$lib/utils/excelParser';
	import { alunos as alunosApi } from '$lib/api';
	import type { ParsedRow, ParseResult } from '$lib/utils/excelParser';

	let steps = ['Upload', 'Mapeamento', 'Validação', 'Importar'];
	let stepAtual = $state(0);

	// Estados
	let arquivo: File | null = $state(null);
	let parseResult: ParseResult | null = $state(null);
	let alunosProcessados: ParsedRow[] = $state([]);
	let importando = $state(false);
	let progresso = $state(0);
	let resultadoImportacao: any = $state(null);
	let erro = $state<string | null>(null);

	function avancar() {
		if (stepAtual < steps.length - 1) stepAtual++;
	}

	function voltar() {
		if (stepAtual > 0) {
			erro = null;
			stepAtual--;
		}
	}

	async function handleUpload(e: Event) {
		const input = e.target as HTMLInputElement;
		const file = input.files?.[0];

		if (!file) return;

		if (!file.name.match(/\.(xlsx|xls|csv)$/i)) {
			erro = 'Arquivo deve ser Excel (.xlsx, .xls) ou CSV (.csv)';
			return;
		}

		try {
			erro = null;
			arquivo = file;
			parseResult = await parseExcelFile(file);
			alunosProcessados = parseResult.data;

			if (alunosProcessados.length === 0) {
				erro = 'Nenhum dado válido encontrado no arquivo';
				return;
			}

			avancar();
		} catch (e) {
			erro = (e as Error).message || 'Erro ao processar arquivo';
		}
	}

	function avancarMapeamento() {
		if (!parseResult) return;

		// Revalidar dados após possível alteração no mapeamento
		alunosProcessados = alunosProcessados.map((aluno) => ({
			...aluno,
			errors: validateRow(aluno)
		}));

		avancar();
	}

	async function executarImportacao() {
		if (!alunosProcessados || alunosProcessados.length === 0) {
			erro = 'Nenhum aluno para importar';
			return;
		}

		const alunosValidos = alunosProcessados.filter((a) => a.errors.length === 0);

		if (alunosValidos.length === 0) {
			erro = 'Todos os alunos possuem erros de validação';
			return;
		}

		try {
			importando = true;
			erro = null;
			progresso = 0;

			// Preparar dados para importação
			const dadosImportacao = alunosValidos.map((aluno) => ({
				nome: aluno.nome,
				turma: aluno.turma,
				cod_turma: aluno.cod_turma,
				chamada: aluno.chamada,
				termo: aluno.termo
			}));

			// Simular progresso
			const intervalo = setInterval(() => {
				if (progresso < 90) {
					progresso += Math.random() * 30;
				}
			}, 200);

			const resultado = await alunosApi.importarLote(dadosImportacao);
			clearInterval(intervalo);

			progresso = 100;
			resultadoImportacao = resultado;
			avancar();
		} catch (e) {
			erro = (e as Error).message || 'Erro ao importar dados';
		} finally {
			importando = false;
		}
	}

	let alunosComErro = $derived(alunosProcessados.filter((a) => a.errors.length > 0));
	let alunosValidos = $derived(alunosProcessados.filter((a) => a.errors.length === 0));
	let taxaErro = $derived(
		alunosProcessados.length > 0
			? Math.round((alunosComErro.length / alunosProcessados.length) * 100)
			: 0
	);
</script>

<div class="flex flex-col gap-2">
	<h1 class="text-2xl font-bold">Importar Alunos</h1>
	<h2 class="text-xl font-normal text-gray-600">
		Faça upload de uma planilha Excel com os dados dos alunos
	</h2>

	<!-- Indicador de Progresso -->
	<div class="flex w-full flex-row items-center justify-between">
		{#each steps as step, i}
			<div class="flex flex-col items-center gap-2">
				<div
					class={i === stepAtual || i < stepAtual
						? 'flex h-10 w-10 items-center justify-center rounded-full bg-red-600 text-white'
						: 'flex h-10 w-10 items-center justify-center rounded-full border border-gray-300 bg-white text-gray-400'}
				>
					{#if i < stepAtual}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							height="24px"
							viewBox="0 -960 960 960"
							width="24px"
							fill="#FFFFFF"
						>
							<path d="M382-240 154-468l57-57 171 171 367-367 57 57-424 424Z" />
						</svg>
					{:else}
						{i + 1}
					{/if}
				</div>
				<p class="text-sm font-semibold {i === stepAtual ? 'text-red-600' : 'text-gray-400'}">
					{step}
				</p>
			</div>

			{#if i < steps.length - 1}
				<div
					class="mb-4 flex-1 border-t {i < stepAtual ? 'border-red-600' : 'border-gray-300'}"
				></div>
			{/if}
		{/each}
	</div>

	<!-- Conteúdo das Etapas -->
	<div class="flex w-full flex-col gap-4 rounded-2xl bg-white p-10 shadow-md">
		<!-- Erro -->
		{#if erro}
			<div class="rounded-lg border border-red-200 bg-red-50 p-4">
				<p class="text-sm font-medium text-red-700">{erro}</p>
			</div>
		{/if}

		<!-- Etapa 0: Upload -->
		{#if stepAtual === 0}
			<label
				class="flex h-80 flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 p-10 transition-colors hover:border-red-400"
			>
				<input
					type="file"
					accept=".xlsx,.xls,.csv"
					onchange={handleUpload}
					class="hidden"
				/>
				<div class="cursor-pointer text-gray-300 transition-colors hover:text-red-600">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						height="60px"
						viewBox="0 -960 960 960"
						width="60px"
						fill="currentColor"
					>
						<path
							d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"
						/>
					</svg>
				</div>
				<p class="text-gray-400">Arraste um arquivo ou clique para fazer upload</p>
				<p class="text-xs text-gray-300">Formatos aceitos: .xlsx, .xls, .csv</p>
				{#if arquivo}
					<p class="mt-4 text-sm font-semibold text-green-600">✓ {arquivo.name}</p>
				{/if}
			</label>

			<!-- Etapa 1: Mapeamento -->
		{:else if stepAtual === 1}
			<div class="space-y-4">
				<div class="rounded-lg bg-blue-50 p-4">
					<p class="text-sm text-blue-700">
						<strong>Total de alunos:</strong> {alunosProcessados.length}
					</p>
				</div>

				<div class="overflow-x-auto">
					<table class="w-full">
						<thead>
							<tr class="border-b border-gray-200">
								<th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Nome</th>
								<th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Turma</th>
								<th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Código Turma</th>
								<th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Chamada</th>
								<th class="px-4 py-2 text-left text-xs font-semibold text-gray-600">Disciplina</th>
							</tr>
						</thead>
						<tbody>
							{#each alunosProcessados.slice(0, 5) as aluno}
								<tr class="border-b border-gray-100">
									<td class="px-4 py-2 text-sm text-gray-700">{aluno.nome}</td>
									<td class="px-4 py-2 text-sm text-gray-700">{aluno.turma}</td>
									<td class="px-4 py-2 text-sm text-gray-700">{aluno.cod_turma}</td>
									<td class="px-4 py-2 text-sm text-gray-700">{aluno.chamada || '—'}</td>
									<td class="px-4 py-2 text-sm text-gray-700">{aluno.disciplina || '—'}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

				{#if alunosProcessados.length > 5}
					<p class="text-center text-xs text-gray-500">
						+{alunosProcessados.length - 5} linhas não exibidas
					</p>
				{/if}

				<div class="flex gap-2">
					<button
						onclick={avancarMapeamento}
						class="flex h-10 flex-1 items-center justify-center rounded border border-red-600 bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
					>
						Avançar
					</button>
					<button
						onclick={voltar}
						class="flex h-10 flex-1 items-center justify-center bg-gray-100 font-medium text-gray-600 transition-colors hover:bg-gray-200"
					>
						Voltar
					</button>
				</div>
			</div>

			<!-- Etapa 2: Validação -->
		{:else if stepAtual === 2}
			<div class="space-y-4">
				<div class="grid grid-cols-3 gap-4">
					<div class="rounded-lg bg-gray-50 p-4">
						<p class="text-xs text-gray-600">Total de Alunos</p>
						<p class="text-2xl font-bold text-gray-900">{alunosProcessados.length}</p>
					</div>
					<div class="rounded-lg bg-green-50 p-4">
						<p class="text-xs text-green-600">Válidos</p>
						<p class="text-2xl font-bold text-green-700">{alunosValidos.length}</p>
					</div>
					<div class="rounded-lg bg-red-50 p-4">
						<p class="text-xs text-red-600">Com Erros</p>
						<p class="text-2xl font-bold text-red-700">{alunosComErro.length}</p>
					</div>
				</div>

				{#if alunosComErro.length > 0}
					<div class="max-h-60 space-y-2 overflow-y-auto rounded-lg border border-red-200 bg-red-50 p-4">
						<p class="font-semibold text-red-700">Erros Encontrados:</p>
						{#each alunosComErro as aluno}
							<div class="border-b border-red-100 pb-2">
								<p class="font-medium text-red-900">Linha {aluno.rowNumber}: {aluno.nome || '(sem nome)'}</p>
								<ul class="ml-4 list-inside list-disc text-xs text-red-700">
									{#each aluno.errors as err}
										<li>{err}</li>
									{/each}
								</ul>
							</div>
						{/each}
					</div>
				{/if}

				{#if alunosValidos.length > 0}
					<div class="rounded-lg border border-green-200 bg-green-50 p-4">
						<p class="font-semibold text-green-700">✓ {alunosValidos.length} aluno(s) pronto(s) para importar</p>
					</div>
				{/if}

				<div class="flex gap-2">
					<button
						disabled={alunosValidos.length === 0}
						onclick={executarImportacao}
						class="flex h-10 flex-1 items-center justify-center rounded border border-red-600 bg-red-600 font-medium text-white transition-colors hover:bg-red-700 disabled:bg-gray-300 disabled:border-gray-300"
					>
						Avançar e Importar
					</button>
					<button
						onclick={voltar}
						class="flex h-10 flex-1 items-center justify-center bg-gray-100 font-medium text-gray-600 transition-colors hover:bg-gray-200"
					>
						Voltar
					</button>
				</div>
			</div>

			<!-- Etapa 3: Importação -->
		{:else if stepAtual === 3}
			<div class="space-y-4">
				{#if importando}
					<div class="space-y-2">
						<p class="font-medium text-gray-700">Importando dados...</p>
						<div class="h-2 w-full overflow-hidden rounded-full bg-gray-200">
							<div
								class="h-full bg-red-600 transition-all"
								style="width: {Math.min(progresso, 100)}%"
							></div>
						</div>
						<p class="text-sm text-gray-500">{Math.round(progresso)}%</p>
					</div>
				{:else if resultadoImportacao}
					<div class="space-y-4">
						<div class="grid grid-cols-3 gap-4">
							<div class="rounded-lg bg-blue-50 p-4">
								<p class="text-xs text-blue-600">Total Processado</p>
								<p class="text-2xl font-bold text-blue-700">{resultadoImportacao.total}</p>
							</div>
							<div class="rounded-lg bg-green-50 p-4">
								<p class="text-xs text-green-600">Sucesso</p>
								<p class="text-2xl font-bold text-green-700">{resultadoImportacao.sucesso}</p>
							</div>
							<div class="rounded-lg bg-red-50 p-4">
								<p class="text-xs text-red-600">Falhas</p>
								<p class="text-2xl font-bold text-red-700">{resultadoImportacao.erro}</p>
							</div>
						</div>

						{#if resultadoImportacao.erro > 0}
							<div class="max-h-48 space-y-2 overflow-y-auto rounded-lg border border-red-200 bg-red-50 p-4">
								<p class="font-semibold text-red-700">Erros na Importação:</p>
								{#each resultadoImportacao.detalhes.filter((d: any) => d.status === 'erro') as detalhe}
									<div class="text-sm text-red-700">
										<p><strong>{detalhe.nome}</strong>: {detalhe.mensagem}</p>
									</div>
								{/each}
							</div>
						{/if}

						<div class="rounded-lg bg-green-100 p-4">
							<p class="text-sm font-medium text-green-800">
								✓ Importação concluída! {resultadoImportacao.sucesso} aluno(s) adicionado(s) com sucesso.
							</p>
						</div>

						<button
							onclick={() => {
								// Reset
								arquivo = null;
								parseResult = null;
								alunosProcessados = [];
								resultadoImportacao = null;
								stepAtual = 0;
								erro = null;
							}}
							class="flex h-10 w-full items-center justify-center rounded border border-red-600 bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
						>
							Importar Novo Arquivo
						</button>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>

