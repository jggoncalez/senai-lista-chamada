<script>
	let { codTurma, nomeTurma, totalAlunos } = $props();
</script>

<div
	class="items-left flex h-auto max-w-md flex-col gap-3 rounded-lg border border-gray-200 p-4 shadow-sm"
>
	<p class="w-20 rounded-xl bg-red-600 p-1 text-center text-sm font-normal text-white">
		{codTurma}
	</p>
	<p class="text-md text-left font-bold">{nomeTurma}</p>
	<div class="flex flex-row items-center gap-2 p-0">
		<p class="w-20 rounded-xl bg-gray-200 p-1 text-center text-sm font-normal">
			{codTurma[0]}ºTermo
		</p>
		<p class="flex flex-row items-center gap-1 text-sm font-normal">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				height="24px"
				viewBox="0 -960 960 960"
				width="24px"
				fill="#dc2626"
			>
				<path
					d="M40-160v-112q0-34 17.5-62.5T104-378q62-31 126-46.5T360-440q66 0 130 15.5T616-378q29 15 46.5 43.5T680-272v112H40Zm720 0v-120q0-44-24.5-84.5T666-434q51 6 96 20.5t84 35.5q36 20 55 44.5t19 53.5v120H760ZM247-527q-47-47-47-113t47-113q47-47 113-47t113 47q47 47 47 113t-47 113q-47 47-113 47t-113-47Zm466 0q-47 47-113 47-11 0-28-2.5t-28-5.5q27-32 41.5-71t14.5-81q0-42-14.5-81T544-792q14-5 28-6.5t28-1.5q66 0 113 47t47 113q0 66-47 113ZM120-240h480v-32q0-11-5.5-20T580-306q-54-27-109-40.5T360-360q-56 0-111 13.5T140-306q-9 5-14.5 14t-5.5 20v32Zm296.5-343.5Q440-607 440-640t-23.5-56.5Q393-720 360-720t-56.5 23.5Q280-673 280-640t23.5 56.5Q327-560 360-560t56.5-23.5ZM360-240Zm0-400Z"
				/>
			</svg>
			{totalAlunos} Alunos
		</p>
	</div>
	<a
		href="/chamada"
		class="flex h-10 w-full items-center justify-center rounded border border-red-600 bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
	>
		Fazer chamada
	</a>
	<a
		href="/relatorio"
		class="flex h-10 w-full items-center justify-center bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
	>
		Ver Relatório
	</a>
</div>
