<script>
	let { nomeTurma, data, diciplina, professor,presentes, totalAlunos } = $props();
	let raio = 54;
	let circunferencia = $derived(2 * Math.PI * raio);
	let progresso = $derived(circunferencia - (presentes / totalAlunos) * circunferencia);
</script>

<div class="flex h-auto w-200 flex-row justify-between rounded-lg p-5 shadow-md">
	<div>
		<p class="text-sm text-gray-500">Turma</p>
		<p class="text-md font-semibold">{nomeTurma}</p>
		<p class="text-sm text-gray-500">Data</p>
		<p class="text-md font-semibold">{data}</p>
		<p class="text-sm text-gray-500">Disciplina</p>
		<p class="text-md font-semibold">{diciplina}</p>
		<p class="text-sm text-gray-500">Professor</p>
		<p class="text-md font-semibold">{professor}</p>
	</div>
	<div>
		<div class="flex items-center justify-center">
			<div class="relative h-40 w-40">
				<svg class="h-full w-full -rotate-90" viewBox="0 0 120 120">
					<!-- Círculo de fundo -->
					<circle cx="60" cy="60" r={raio} fill="none" stroke="#e5e7eb" stroke-width="10" />
					<!-- Círculo de progresso -->
					<circle
						cx="60"
						cy="60"
						r={raio}
						fill="none"
						stroke="#16a34a"
						stroke-width="10"
						stroke-linecap="round"
						stroke-dasharray={circunferencia}
						stroke-dashoffset={progresso}
						class="transition-all duration-500"
					/>
				</svg>

				<!-- Texto do centro -->
				<div class="absolute inset-0 flex flex-col items-center justify-center">
					<span class="text-xl font-bold text-gray-800"
						>{presentes} / {totalAlunos}</span
					>
					<span class="text-xs text-gray-400">presentes</span>
					<span class="text-sm font-semibold text-green-600">
						 {totalAlunos > 0 ? ((presentes / totalAlunos) * 100).toFixed(0) : 0}%
					</span>
				</div>
			</div>
		</div>
	</div>
</div>
