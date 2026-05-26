<script lang="ts">
	import { onMount } from 'svelte';
	import { turmas as turmasApi, chamadas as chamadasApi } from '$lib/api';
	import type { ChamadaItem, TurmaItem } from '$lib/api';

	import ExcelJS from 'exceljs';

	// CORREÇÃO DO VITE: Importando o pacote completo CommonJS para extrair o saveAs
	import fileSaverPkg from 'file-saver';
	const { saveAs } = fileSaverPkg;

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
		const registros = chamadaTurma.filter((c) => c.nome_aluno === nomeAluno && c.cod_turma === cod);
		if (!registros.length) return 0;
		return Math.round((registros.filter((c) => c.presente).length / registros.length) * 100);
	}

	function formatarDataBR(dataUS: string) {
		if (!dataUS) return '';
		const [ano, mes, dia] = dataUS.split('-');
		return `${dia}/${mes}/${ano}`;
	}

	async function exportarExcelComCores() {
		if (alunosUnicos.length === 0) {
			alert('Selecione uma turma com dados para exportar.');
			return;
		}

		const workbook = new ExcelJS.Workbook();
		const worksheet = workbook.addWorksheet('Frequência');

		// 1. Calcular dinamicamente a última coluna com base no número de datas
		// Coluna 1 (Nº) + Coluna 2 (Nome) + Quantidade de Datas + Coluna Final (% Frequência)
		const totalColunasNum = 2 + datas.length + 1;

		// Converter o número de colunas para a letra correspondente do Excel (Ex: 5 -> 'E', 8 -> 'H')
		const ultimaLetraColuna = String.fromCharCode(64 + totalColunasNum);

		// Mesclar dinamicamente da célula A1 até a última coluna calculada nas linhas 1 e 2
		worksheet.mergeCells(`A1:${ultimaLetraColuna}2`);

		const titleCell = worksheet.getCell('A1');
		titleCell.value = 'SENAI - DIÁRIO DE CLASSE (RELATÓRIO DE FREQUÊNCIA)';
		titleCell.font = { name: 'Arial', size: 14, bold: true, color: { argb: 'FFFFFF' } };
		titleCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'B91C1C' } }; // Vermelho SENAI
		titleCell.alignment = { horizontal: 'center', vertical: 'middle' };

		worksheet.addRow([]);
		worksheet.addRow(['Turma:', cod]);
		worksheet.addRow(['Período:', `${formatarDataBR(datainicio)} até ${formatarDataBR(datafim)}`]);
		const disciplinaLabel =
			disciplinaSelecionada === 'todas' ? 'Todas' : disciplinaSelecionada || 'Todas';
		worksheet.addRow(['Disciplina:', disciplinaLabel]);
		worksheet.addRow([]);

		['A4', 'A5', 'A6'].forEach((cellId) => {
			worksheet.getCell(cellId).font = { bold: true, color: { argb: '475569' } };
		});

		const colunasHeaders = [
			'Nº',
			'Nome do Aluno',
			...datas.map((d) => d.slice(5).replace('-', '/')),
			'% Frequência'
		];
		const headerRow = worksheet.addRow(colunasHeaders);

		headerRow.eachCell((cell) => {
			cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: '475569' } };
			cell.font = { name: 'Arial', size: 10, bold: true, color: { argb: 'FFFFFF' } };
			cell.alignment = { horizontal: 'center', vertical: 'middle' };
		});

		alunosUnicos.forEach((nomeAluno, idx) => {
			const pct = getPorcentagem(nomeAluno);
			const dadosLinha = [
				idx + 1,
				nomeAluno,
				...datas.map((data) => {
					const p = getPresenca(nomeAluno, data);
					return p === true ? '✓' : p === false ? '✕' : '—';
				}),
				`${pct}%`
			];

			const row = worksheet.addRow(dadosLinha);
			const corFundoRow = idx % 2 === 0 ? 'F8FAFC' : 'FFFFFF';

			row.eachCell((cell, colNumber) => {
				cell.border = {
					top: { style: 'thin', color: { argb: 'E2E8F0' } },
					bottom: { style: 'thin', color: { argb: 'E2E8F0' } },
					left: { style: 'thin', color: { argb: 'E2E8F0' } },
					right: { style: 'thin', color: { argb: 'E2E8F0' } }
				};

				cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: corFundoRow } };

				if (colNumber === 1) cell.alignment = { horizontal: 'center' };
				if (colNumber === 2) cell.alignment = { horizontal: 'left' };

				if (colNumber > 2 && colNumber < colunasHeaders.length) {
					cell.alignment = { horizontal: 'center' };
					if (cell.value === '✓') {
						cell.font = { bold: true, color: { argb: '166534' } };
						cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'DCFCE7' } };
					} else if (cell.value === '✕') {
						cell.font = { bold: true, color: { argb: '991B1B' } };
						cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FEE2E2' } };
					}
				}

				if (colNumber === colunasHeaders.length) {
					cell.alignment = { horizontal: 'center' };
					cell.font = { bold: true, color: { argb: pct >= 75 ? '166534' : '991B1B' } };
				}
			});
		});

		worksheet.columns.forEach((column) => {
			let maxLength = 0;
			column.eachCell!({ includeEmpty: true }, (cell) => {
				const columnLength = cell.value ? cell.value.toString().length : 0;
				if (columnLength > maxLength) maxLength = columnLength;
			});
			column.width = maxLength < 10 ? 10 : maxLength + 3;
		});

		const buffer = await workbook.xlsx.writeBuffer();
		saveAs(new Blob([buffer]), `Relatorio_SENAI_Turma_${cod || 'Geral'}.xlsx`);
	}
</script>

<div class="flex flex-col gap-2 print:hidden">
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

	<div
		class="mb-4 flex flex-col gap-6 rounded-xl border border-gray-200 bg-white p-6 shadow-sm md:flex-row md:items-center"
	>
		<div class="flex min-w-48 flex-col gap-1">
			<label class="text-xs font-semibold tracking-wide text-gray-400 uppercase">Turma</label>
			<select
				bind:value={cod}
				class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-700 focus:outline-none"
			>
				<option value="">Selecione...</option>
				{#each codTurmas as codigo}
					<option value={codigo}>{codigo}</option>
				{/each}
			</select>
		</div>
		<div class="flex flex-col gap-1">
			<label class="text-xs font-semibold tracking-wide text-gray-400 uppercase">Data Início</label>
			<input
				type="date"
				bind:value={datainicio}
				class="rounded-lg border border-gray-200 px-3 py-2 text-sm text-gray-700 focus:outline-none"
			/>
		</div>
		<div class="flex flex-col gap-1">
			<label class="text-xs font-semibold tracking-wide text-gray-400 uppercase">Data Fim</label>
			<input
				type="date"
				bind:value={datafim}
				class="rounded-lg border border-gray-200 px-3 py-2 text-sm text-gray-700 focus:outline-none"
			/>
		</div>
		<div class="flex min-w-48 flex-col gap-1">
			<label class="text-xs font-semibold tracking-wide text-gray-400 uppercase">Disciplina</label>
			<select
				bind:value={disciplinaSelecionada}
				class="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-700 focus:outline-none"
			>
				<option value="">Selecione...</option>
				<option value="todas">Todas</option>
				{#each disciplinas as d}
					<option value={d}>{d}</option>
				{/each}
			</select>
		</div>
	</div>
</div>

<div
	id="print-area"
	class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm print:border-none print:shadow-none"
>
	<div class="mb-4 hidden rounded-t-lg bg-red-700 px-4 py-5 text-center text-white print:block">
		<h1 class="m-0 text-2xl font-bold tracking-wider">SENAI - DIÁRIO DE CLASSE</h1>
		<p class="m-0 mt-1 text-xs opacity-90">Relatório de Frequência de Alunos</p>
	</div>

	<div class="mb-4 hidden border-b-2 border-gray-200 px-2 pb-3 text-xs text-gray-700 print:block">
		<div class="grid grid-cols-3 gap-2">
			<p><span class="font-bold text-gray-500">Turma:</span> {cod || '—'}</p>
			<p>
				<span class="font-bold text-gray-500">Período:</span>
				{formatarDataBR(datainicio)} até {formatarDataBR(datafim)}
			</p>
			<p>
				<span class="font-bold text-gray-500">Disciplina:</span>
				{disciplinaSelecionada === 'todas' || !disciplinaSelecionada
					? 'Todas'
					: disciplinaSelecionada}
			</p>
		</div>
	</div>

	{#if alunosUnicos.length > 0}
		<div
			class="mx-2 mb-4 hidden rounded-lg border border-gray-200 bg-gray-50 p-3 text-xs print:block"
		>
			<div class="grid grid-cols-3 text-center">
				<div>
					<span class="block font-medium text-gray-500">Total de Alunos</span>
					<span class="text-base font-bold text-gray-800">{alunosUnicos.length}</span>
				</div>
				<div>
					<span class="block font-medium text-gray-500">Presentes</span>
					<span class="text-base font-bold text-green-700">{presentes}</span>
				</div>
				<div>
					<span class="block font-medium text-gray-500">Ausentes</span>
					<span class="text-base font-bold text-red-600">{ausentes}</span>
				</div>
			</div>
		</div>
	{/if}

	<div class="w-full overflow-x-auto">
		<table class="w-full border-collapse">
			<thead>
				<tr class="border-b border-gray-200 bg-slate-600 text-white">
					<th class="w-12 px-4 py-3 text-left text-xs font-semibold uppercase">Nº</th>
					<th class="px-6 py-3 text-left text-xs font-semibold uppercase">Nome do Aluno</th>
					{#each datas as data}
						<th class="px-2 py-3 text-center text-xs font-semibold uppercase">
							{data.slice(5).replace('-', '/')}
						</th>
					{/each}
					<th class="w-24 px-4 py-3 text-right text-xs font-semibold uppercase">% Freq.</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-gray-100">
				{#each alunosUnicos as nomeAluno, i}
					{@const pct = getPorcentagem(nomeAluno)}
					<tr class="odds:bg-gray-50/20 hover:bg-slate-50/50">
						<td class="px-4 py-3 text-sm font-semibold text-red-600/80">{i + 1}</td>
						<td class="px-6 py-4 text-sm font-medium text-gray-800">{nomeAluno}</td>

						{#each datas as data}
							{@const presente = getPresenca(nomeAluno, data)}
							<td class="px-2 py-3 text-center">
								{#if presente === true}
									<span
										class="inline-flex items-center justify-center rounded-md bg-green-100 px-2 py-0.5 text-xs font-bold text-green-700 print:bg-green-100 print:text-green-700"
										>✓</span
									>
								{:else if presente === false}
									<span
										class="inline-flex items-center justify-center rounded-md bg-red-100 px-2 py-0.5 text-xs font-bold text-red-700 print:bg-red-100 print:text-red-700"
										>✕</span
									>
								{:else}
									<span class="font-light text-gray-300">—</span>
								{/if}
							</td>
						{/each}

						<td class="px-4 py-3 text-right">
							<span
								class="inline-block rounded-lg px-2 py-0.5 text-xs font-bold text-white shadow-sm {pct >=
								75
									? 'bg-green-600'
									: 'bg-red-500'} print:bg-transparent print:text-sm print:text-gray-900 print:shadow-none"
							>
								{pct}%
							</span>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	{#if alunosUnicos.length === 0}
		<div class="py-16 text-center text-sm font-medium text-gray-400 print:hidden">
			Selecione uma turma ativa para visualizar os diários de chamada.
		</div>
	{/if}
</div>

<style>
	@media print {
		/* PEGA RÍGIDO: Remove absolutamente QUALQUER div/elemento que pertença 
      à estrutura externa do layout (+layout.svelte) de forma global
    */
		:global(body *),
		:global(html *) {
			visibility: hidden !important;
		}

		/* Diz para o navegador reativar a visibilidade EXCLUSIVAMENTE para o bloco 
      do relatório (#print-area) e tudo o que estiver dentro dele!
    */
		#print-area,
		#print-area * {
			visibility: visible !important;
		}

		/* Reposiciona o elemento isolado no topo absoluto do papel A4 */
		#print-area {
			position: absolute !important;
			left: 0 !important;
			top: 0 !important;
			width: 100% !important;
			margin: 0 !important;
			padding: 0 !important;
		}

		/* Remove o espaçamento (padding/background) injetado na tag <main> pelo layout */
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
