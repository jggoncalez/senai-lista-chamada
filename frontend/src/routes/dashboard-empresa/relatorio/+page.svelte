<script lang="ts">
	import { onMount } from 'svelte';
	import { chamadas as chamadasApi } from '$lib/api';
	import type { ChamadaItem } from '$lib/api';
	import { goto } from '$app/navigation';
	import ExcelJS from 'exceljs';
	import fileSaverPkg from 'file-saver';
	const { saveAs } = fileSaverPkg;

	let companyName = $state('');
	let datainicio = $state(
		new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split('T')[0]
	);
	let datafim = $state(new Date().toISOString().split('T')[0]);
	let disciplinaSelecionada = $state('todas');
	let chamadaEmpresa = $state<ChamadaItem[]>([]);
	let carregando = $state(true);

	onMount(async () => {
		const loggedIn = localStorage.getItem('company_logged_in');
		if (!loggedIn) {
			goto('/login-empresa');
			return;
		}
		companyName = localStorage.getItem('company_name') || '';
		await carregarDados();
	});

	async function carregarDados() {
		try {
			carregando = true;
			chamadaEmpresa = await chamadasApi.listarPorEmpresa(companyName, datainicio, datafim);
		} catch (e) {
			console.error('Erro ao carregar dados:', e);
			chamadaEmpresa = [];
		} finally {
			carregando = false;
		}
	}

	let disciplinas = $derived([...new Set(chamadaEmpresa.map((c) => c.disciplina))].sort());

	let alunosFiltrados = $derived(
		chamadaEmpresa.filter((c) => {
			const dataAula = c.data_aula.slice(0, 10);
			const dataOk = dataAula >= datainicio && dataAula <= datafim;
			const discOk = disciplinaSelecionada === 'todas' || c.disciplina === disciplinaSelecionada;
			return dataOk && discOk;
		})
	);

	let alunosUnicos = $derived([...new Set(alunosFiltrados.map((c) => c.nome_aluno))]);
	let datas = $derived([...new Set(alunosFiltrados.map((c) => c.data_aula.slice(0, 10)))].sort());

	let alunoInfoMap = $derived(
		alunosFiltrados.reduce(
			(acc, c) => {
				if (!acc[c.nome_aluno]) {
					acc[c.nome_aluno] = { chamada: c.chamada, turma: c.cod_turma };
				}
				return acc;
			},
			{} as Record<string, { chamada?: number | null; turma: string }>
		)
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
		return chamadaEmpresa.filter(
			(c) => c.nome_aluno === nomeAluno && c.disciplina === disc && !c.presente
		).length;
	}

	function formatarDataBR(dataUS: string) {
		if (!dataUS) return '';
		const [ano, mes, dia] = dataUS.split('-');
		return `${dia}/${mes}/${ano}`;
	}

	function exportarPDF() {
		window.print();
	}

	async function exportarExcelComCores() {
		const workbook = new ExcelJS.Workbook();
		const worksheet = workbook.addWorksheet('Relatório Empresa');

		worksheet.mergeCells(`A1:${String.fromCharCode(64 + 2 + datas.length + 1)}2`);
		const titleCell = worksheet.getCell('A1');
		titleCell.value = `SENAI - RELATÓRIO DE FREQUÊNCIA — ${companyName}`;
		titleCell.font = { name: 'Arial', size: 13, bold: true, color: { argb: 'FFFFFF' } };
		titleCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'B91C1C' } };
		titleCell.alignment = { horizontal: 'center', vertical: 'middle' };

		worksheet.addRow([]);
		worksheet.addRow(['Empresa:', companyName]);
		worksheet.addRow(['Período:', `${formatarDataBR(datainicio)} até ${formatarDataBR(datafim)}`]);
		worksheet.addRow([]);

		const headers = [
			'Nº',
			'Aluno',
			'Turma',
			...datas.map((d) => d.slice(5).replace('-', '/')),
			'% Freq.'
		];
		const headerRow = worksheet.addRow(headers);
		headerRow.eachCell((cell) => {
			cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: '475569' } };
			cell.font = { bold: true, color: { argb: 'FFFFFF' } };
			cell.alignment = { horizontal: 'center' };
		});

		alunosUnicos.forEach((nome, idx) => {
			const info = alunoInfoMap[nome];
			const freq = getFrequenciaMedia(nome);
			const row = worksheet.addRow([
				info?.chamada ?? idx + 1,
				nome,
				info?.turma ?? '—',
				...datas.map((d) => {
					const p = getPresenca(nome, d);
					return p === true ? '✓' : p === false ? '✕' : '—';
				}),
				`${freq}%`
			]);

			row.eachCell((cell, col) => {
				cell.border = {
					top: { style: 'thin', color: { argb: 'E2E8F0' } },
					bottom: { style: 'thin', color: { argb: 'E2E8F0' } },
					left: { style: 'thin', color: { argb: 'E2E8F0' } },
					right: { style: 'thin', color: { argb: 'E2E8F0' } }
				};
				if (col > 3 && col < headers.length) {
					cell.alignment = { horizontal: 'center' };
					if (cell.value === '✓') {
						cell.font = { bold: true, color: { argb: '166534' } };
						cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'DCFCE7' } };
					} else if (cell.value === '✕') {
						cell.font = { bold: true, color: { argb: '991B1B' } };
						cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FEE2E2' } };
					}
				}
				if (col === headers.length) {
					cell.font = { bold: true, color: { argb: freq >= 75 ? '166534' : '991B1B' } };
					cell.alignment = { horizontal: 'center' };
				}
			});
		});

		worksheet.columns.forEach((col) => {
			let max = 10;
			col.eachCell!({ includeEmpty: true }, (cell) => {
				const len = cell.value ? cell.value.toString().length : 0;
				if (len > max) max = len;
			});
			col.width = max + 3;
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
				onclick={exportarPDF}
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
	<div class="flex flex-col gap-1">
		<label for="datainicio" class="text-xs font-semibold tracking-wide text-gray-400 uppercase"
			>Data Início</label
		>
		<input
			id="datainicio"
			type="date"
			bind:value={datainicio}
			onchange={carregarDados}
			class="rounded-lg border border-gray-200 p-2 text-sm"
		/>
	</div>
	<div class="flex flex-col gap-1">
		<label for="datafim" class="text-xs font-semibold tracking-wide text-gray-400 uppercase"
			>Data Fim</label
		>
		<input
			id="datafim"
			type="date"
			bind:value={datafim}
			onchange={carregarDados}
			class="rounded-lg border border-gray-200 p-2 text-sm"
		/>
	</div>
	<div class="flex flex-col gap-1">
		<label for="disciplina" class="text-xs font-bold text-gray-400 uppercase">Disciplina</label>
		<select
			id="disciplina"
			bind:value={disciplinaSelecionada}
			class="rounded-lg border border-gray-200 bg-white p-2 text-sm"
		>
			<option value="todas">Todas as Disciplinas</option>
			{#each disciplinas as d}
				<option value={d}>{d}</option>
			{/each}
		</select>
	</div>

	<!-- Tabela de Frequência -->
	<div
		id="print-area"
		class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm print:border-none print:shadow-none"
	>
		<!-- Cabeçalho visível apenas no print -->
		<div class="mb-4 hidden rounded-t-lg bg-red-700 px-4 py-5 text-center text-white print:block">
			<h1 class="m-0 text-2xl font-bold tracking-wider">SENAI - RELATÓRIO DE PRESENÇA</h1>
			<p class="m-0 mt-1 text-xs opacity-90">{companyName}</p>
		</div>
		<div class="mb-4 hidden border-b-2 border-gray-200 px-2 pb-3 text-xs text-gray-700 print:block">
			<div class="grid grid-cols-2 gap-2">
				<p><span class="font-bold text-gray-500">Empresa:</span> {companyName}</p>
				<p>
					<span class="font-bold text-gray-500">Período:</span>
					{formatarDataBR(datainicio)} até {formatarDataBR(datafim)}
				</p>
			</div>
		</div>

		<div class="flex items-center justify-between border-b border-gray-100 p-6 print:hidden">
			<h3 class="font-bold text-gray-700">Frequência Diária</h3>
			<span class="text-xs text-gray-400">{alunosUnicos.length} alunos vinculados</span>
		</div>
		<div class="overflow-x-auto">
			<table class="w-full border-collapse text-left">
				<thead>
					<tr class="bg-gray-50">
						<th class="border-b px-6 py-4 text-xs font-bold text-gray-500 uppercase">Nº</th>
						<th class="border-b px-6 py-4 text-xs font-bold text-gray-500 uppercase">Aluno</th>
						<th class="border-b px-6 py-4 text-center text-xs font-bold text-gray-500 uppercase"
							>Turma</th
						>
						{#each datas as data}
							<th
								class="min-w-[60px] border-b px-3 py-4 text-center text-xs font-bold text-gray-500 uppercase"
							>
								{data.slice(8)}/{data.slice(5, 7)}
							</th>
						{/each}
						<th class="border-b px-6 py-4 text-right text-xs font-bold text-gray-500 uppercase"
							>Média</th
						>
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
								<span class="rounded bg-blue-50 px-2 py-1 text-xs font-bold text-blue-600">
									{info?.turma}
								</span>
							</td>
							{#each datas as data}
								{@const p = getPresenca(nome, data)}
								<td class="px-3 py-4 text-center">
									{#if p === true}
										<span class="font-bold text-green-600">✓</span>
									{:else if p === false}
										<span class="font-bold text-red-500">✕</span>
									{:else}
										<span class="text-gray-300">-</span>
									{/if}
								</td>
							{/each}
							<td
								class="px-6 py-4 text-right font-bold {freq >= 75
									? 'text-green-600'
									: 'text-red-600'}"
							>
								{freq}%
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>

	<!-- Detalhamento de Faltas por Disciplina -->
	<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
		{#each alunosUnicos as nome}
			<div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
				<div class="flex items-center justify-between border-b border-gray-200 bg-gray-50 p-4">
					<h4 class="font-bold text-gray-700">{nome}</h4>
					<span class="text-xs font-medium text-gray-500">{alunoInfoMap[nome]?.turma}</span>
				</div>
				<div class="p-4">
					<p class="mb-3 text-xs font-bold text-gray-400 uppercase">Faltas por Disciplina</p>
					<div class="space-y-3">
						{#each disciplinas as disc}
							{@const faltas = getFaltasPorDisciplina(nome, disc)}
							<div class="flex items-center justify-between">
								<span class="text-sm text-gray-600">{disc}</span>
								<div class="flex items-center gap-3">
									<div class="h-2 w-32 overflow-hidden rounded-full bg-gray-100">
										<div
											class="h-full bg-red-500"
											style="width: {Math.min(faltas * 10, 100)}%"
										></div>
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
		:global(body *),
		:global(html *) {
			visibility: hidden !important;
		}

		#print-area,
		#print-area * {
			visibility: visible !important;
		}

		#print-area {
			position: absolute !important;
			left: 0 !important;
			top: 0 !important;
			width: 100% !important;
			margin: 0 !important;
			padding: 0 !important;
		}

		:global(main) {
			padding: 0 !important;
			margin: 0 !important;
			background: white !important;
		}

		@page {
			size: A4 landscape;
			margin: 8mm 10mm;
		}

		:global(body) {
			-webkit-print-color-adjust: exact !important;
			print-color-adjust: exact !important;
			background-color: white !important;
		}
	}
</style>
