<script lang="ts">
	import { onMount } from 'svelte';
	import { chamadas as chamadasApi } from '$lib/api';
	import type { ChamadaItem } from '$lib/api';
	import { goto } from '$app/navigation';
	import ExcelJS from 'exceljs';
	import fileSaverPkg from 'file-saver';
	const { saveAs } = fileSaverPkg;

	let companyName = $state('');
	let datainicio = $state(new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split('T')[0]);
	let datafim = $state(new Date().toISOString().split('T')[0]);
	let disciplinaSelecionada = $state('todas');
	let chamadaEmpresa = $state<ChamadaItem[]>([]);
	let carregando = $state(true);

	onMount(async () => {
		const loggedIn = localStorage.getItem('company_logged_in');
		if (!loggedIn) {
			// Para propósitos de desenvolvimento, se não estiver logado, pegamos um mock
			companyName = 'Empresa Exemplo';
		} else {
			companyName = localStorage.getItem('company_name') || 'Empresa';
		}
		await carregarDados();
	});

	async function carregarDados() {
		try {
			carregando = true;
			// Chamada para o novo endpoint de empresa
			chamadaEmpresa = await chamadasApi.listarPorEmpresa(companyName);
		} catch (e) {
			console.error('Erro ao carregar dados da empresa:', e);
			// Fallback mock para visualização se o backend estiver fora
			chamadaEmpresa = [
				{ id: 1, nome_aluno: 'João Silva', cod_turma: 'MEC-2024', disciplina: 'Mecânica Aplicada', data_aula: '2024-05-20', presente: true, chamada: 1 },
				{ id: 2, nome_aluno: 'João Silva', cod_turma: 'MEC-2024', disciplina: 'Mecânica Aplicada', data_aula: '2024-05-21', presente: false, chamada: 1 },
				{ id: 3, nome_aluno: 'Maria Oliveira', cod_turma: 'MEC-2024', disciplina: 'Mecânica Aplicada', data_aula: '2024-05-20', presente: true, chamada: 2 },
				{ id: 4, nome_aluno: 'Maria Oliveira', cod_turma: 'MEC-2024', disciplina: 'Matemática', data_aula: '2024-05-22', presente: true, chamada: 2 },
			];
		} finally {
			carregando = false;
		}
	}

	let disciplinas = $derived([...new Set(chamadaEmpresa.map((c) => c.disciplina))].sort());

	let alunosFiltrados = $derived(
		chamadaEmpresa.filter((c) => {
			const dataAula = c.data_aula.slice(0, 10);
			const dataOk = dataAula >= datainicio && dataAula <= datafim;
			const discOk =
				disciplinaSelecionada === 'todas' ||
				c.disciplina === disciplinaSelecionada;
			return dataOk && discOk;
		})
	);

	let alunosUnicos = $derived([...new Set(alunosFiltrados.map((c) => c.nome_aluno))]);
	let datas = $derived([...new Set(alunosFiltrados.map((c) => c.data_aula.slice(0, 10)))].sort());

	let alunoInfoMap = $derived(
		alunosFiltrados.reduce((acc, c) => {
			if (!acc[c.nome_aluno]) {
				acc[c.nome_aluno] = { 
					chamada: c.chamada,
					turma: c.cod_turma
				};
			}
			return acc;
		}, {} as Record<string, { chamada?: number | null, turma: string }>)
	);

	function getPresenca(nomeAluno: string, data: string): boolean | null {
		const registro = alunosFiltrados.find(
			(c) => c.nome_aluno === nomeAluno && c.data_aula.slice(0, 10) === data
		);
		return registro ? registro.presente : null;
	}

	function getFrequenciaMedia(nomeAluno: string): number {
		const registros = chamadaEmpresa.filter((c) => c.nome_aluno === nomeAluno);
		if (!registros.length) return 0;
		return Math.round((registros.filter((c) => c.presente).length / registros.length) * 100);
	}

	function getFaltasPorDisciplina(nomeAluno: string, disc: string): number {
		return chamadaEmpresa.filter(c => c.nome_aluno === nomeAluno && c.disciplina === disc && !c.presente).length;
	}

	function formatarDataBR(dataUS: string) {
		if (!dataUS) return '';
		const [ano, mes, dia] = dataUS.split('-');
		return `${dia}/${mes}/${ano}`;
	}

	function handleLogout() {
		localStorage.removeItem('company_logged_in');
		localStorage.removeItem('company_name');
		goto('/selecao');
	}

	async function exportarExcel() {
		const workbook = new ExcelJS.Workbook();
		const worksheet = workbook.addWorksheet('Relatório Empresa');

		worksheet.addRow(['Relatório de Frequência - ' + companyName]);
		worksheet.addRow(['Período:', `${formatarDataBR(datainicio)} até ${formatarDataBR(datafim)}`]);
		worksheet.addRow([]);

		const headers = ['Nº', 'Aluno', 'Turma', 'Freq. Média (%)', ...datas.map(d => formatarDataBR(d))];
		worksheet.addRow(headers);

		alunosUnicos.forEach((nome, idx) => {
			const info = alunoInfoMap[nome];
			const freq = getFrequenciaMedia(nome);
			const rowData = [
				info?.chamada ?? idx + 1,
				nome,
				info?.turma,
				freq + '%',
				...datas.map(d => {
					const p = getPresenca(nome, d);
					return p === true ? 'P' : p === false ? 'F' : '-';
				})
			];
			worksheet.addRow(rowData);
		});

		const buffer = await workbook.xlsx.writeBuffer();
		saveAs(new Blob([buffer]), `Relatorio_${companyName}.xlsx`);
	}
</script>

<div class="flex flex-col gap-6">
<div class="flex items-center justify-between">
		<h1 class="text-2xl font-bold text-gray-800">Relatório de Presença</h1>
		<div class="flex gap-3">
			<button
				onclick={() => window.print()}
				class="flex h-10 cursor-pointer items-center justify-center gap-2 rounded-xl border border-red-600 bg-white px-4 font-medium text-red-600 shadow-sm transition-colors hover:bg-red-600 hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="20px"
					viewBox="0 -960 960 960"
					width="20px"
					fill="currentColor"
				>
					<path
						d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"
					/>
				</svg>
				Exportar PDF
			</button>

			<button
				onclick={exportarExcelComCores}
				class="flex h-10 cursor-pointer items-center justify-center gap-2 rounded-xl border border-red-600 bg-white px-4 font-medium text-red-600 shadow-sm transition-colors hover:bg-red-600 hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="20px"
					viewBox="0 -960 960 960"
					width="20px"
					fill="currentColor"
				>
					<path
						d="M440-120v-480H120v-160q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H440Zm80-80h240v-160H520v160Zm0-240h240v-160H520v160ZM200-680h560v-80H200v80ZM120-80v-80h102q-48-23-77.5-68T115-330q0-79 55.5-134.5T305-520v80q-45 0-77.5 32T195-330q0 39 24 69t61 38v-97h80v240H120Z"
					/>
				</svg>
				Exportar Excel
			</button>
		</div>
	</div>
	<!-- Filtros -->
	<div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 grid grid-cols-1 md:grid-cols-4 gap-4 print:hidden">
		<div class="flex flex-col gap-1">
			<label class="text-xs font-semibold tracking-wide text-gray-400 uppercase">Data Início</label>
			<input type="date" bind:value={datainicio} class="border border-gray-200 rounded-lg p-2 text-sm">
		</div>
		<div class="flex flex-col gap-1">
			<label class="text-xs font-semibold tracking-wide text-gray-400 uppercase">Data Fim</label>
			<input type="date" bind:value={datafim} class="border border-gray-200 rounded-lg p-2 text-sm">
		</div>
		<div class="flex min-w-48 flex-col gap-1">
			<label class="text-xs font-bold text-gray-400 uppercase">Disciplina</label>
			<select bind:value={disciplinaSelecionada} class="border border-gray-200 rounded-lg p-2 text-sm bg-white">
				<option value="todas">Todas as Disciplinas</option>
				{#each disciplinas as d}
					<option value={d}>{d}</option>
				{/each}
			</select>
		</div>
	</div>

	<!-- Tabela de Frequência -->
	<div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
		<div class="p-6 border-b border-gray-100 flex justify-between items-center">
			<h3 class="font-bold text-gray-700">Frequência Diária</h3>
			<span class="text-xs text-gray-400">{alunosUnicos.length} alunos vinculados</span>
		</div>
		<div class="overflow-x-auto">
			<table class="w-full text-left border-collapse">
				<thead>
					<tr class="bg-gray-50">
						<th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase border-b">Nº</th>
						<th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase border-b">Aluno</th>
						<th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase border-b text-center">Turma</th>
						{#each datas as data}
							<th class="px-3 py-4 text-xs font-bold text-gray-500 uppercase border-b text-center min-w-[60px]">
								{data.slice(8)}/{data.slice(5, 7)}
							</th>
						{/each}
						<th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase border-b text-right">Média</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-100">
					{#each alunosUnicos as nome, i}
						{@const info = alunoInfoMap[nome]}
						{@const freq = getFrequenciaMedia(nome)}
						<tr class="hover:bg-gray-50/50">
							<td class="px-6 py-4 text-sm text-gray-400">{info?.chamada ?? i + 1}</td>
							<td class="px-6 py-4 font-medium text-gray-800">{nome}</td>
							<td class="px-6 py-4 text-center">
								<span class="text-xs font-bold bg-blue-50 text-blue-600 px-2 py-1 rounded">
									{info?.turma}
								</span>
							</td>
							{#each datas as data}
								{@const p = getPresenca(nome, data)}
								<td class="px-3 py-4 text-center">
									{#if p === true}
										<span class="text-green-600 font-bold">✓</span>
									{:else if p === false}
										<span class="text-red-500 font-bold">✕</span>
									{:else}
										<span class="text-gray-300">-</span>
									{/if}
								</td>
							{/each}
							<td class="px-6 py-4 text-right font-bold {freq >= 75 ? 'text-green-600' : 'text-red-600'}">
								{freq}%
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>

	<!-- Detalhamento de Faltas por Disciplina -->
	<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
		{#each alunosUnicos as nome}
			<div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
				<div class="p-4 bg-gray-50 border-b border-gray-200 flex justify-between items-center">
					<h4 class="font-bold text-gray-700">{nome}</h4>
					<span class="text-xs font-medium text-gray-500">{alunoInfoMap[nome]?.turma}</span>
				</div>
				<div class="p-4">
					<p class="text-xs font-bold text-gray-400 uppercase mb-3">Faltas por Disciplina</p>
					<div class="space-y-3">
						{#each disciplinas as disc}
							{@const faltas = getFaltasPorDisciplina(nome, disc)}
							<div class="flex items-center justify-between">
								<span class="text-sm text-gray-600">{disc}</span>
								<div class="flex items-center gap-3">
									<div class="w-32 h-2 bg-gray-100 rounded-full overflow-hidden">
										<div class="h-full bg-red-500" style="width: {Math.min(faltas * 10, 100)}%"></div>
									</div>
									<span class="text-xs font-bold {faltas > 0 ? 'text-red-600' : 'text-gray-400'}">
										{faltas} faltas
									</span>
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	@media print {
		header, .print\:hidden {
			display: none !important;
		}
		main {
			padding: 0 !important;
		}
		.bg-white {
			border: none !important;
			box-shadow: none !important;
		}
	}
</style>
