<script>
	let steps = ['Upload', 'Mapeamento', 'Validação', 'Importar'];
	let stepAtual = $state(0);
	function avancar() {
		if (stepAtual < steps.length - 1) stepAtual++;
	}
	function voltar() {
		if (stepAtual > 0) stepAtual--;
	}
</script>

<div class="flex flex-col gap-2">
	<h1 class="text-2xl font-bold">Importar Alunos</h1>
	<h2 class="text-xl font-normal text-gray-600">
		Faça upload de uma planilha Excel com os dados dos alunos
	</h2>
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
	<div class="flex w-full flex-col gap-4 rounded-2xl bg-white p-10 shadow-md">
		{#if stepAtual == 0}
			<button
				onclick={avancar}
				class="flex h-80 flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 p-10 transition-colors hover:border-red-400"
			>
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
			</button>
		{:else if stepAtual == 1}
			<div
				class="flex h-80 w-full flex-col items-center justify-center gap-4 rounded-xl bg-white p-10 shadow-md"
			></div>
			<button
				onclick={avancar}
				class="flex h-10 w-full items-center justify-center rounded border border-red-600 bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
			>
				Avançar
			</button>
			<button
				onclick={voltar}
				class="flex h-10 w-full items-center justify-center bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
			>
				Voltar
			</button>
		{:else if stepAtual == 2}
			<div
				class="flex h-80 w-full flex-col items-center justify-center gap-4 rounded-xl bg-white p-10 shadow-md"
			>
            	</div>
				<button
					onclick={avancar}
					class="flex h-10 w-full items-center justify-center rounded border border-red-600 bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
				>
					Avançar
				</button>
				<button
					onclick={voltar}
					class="flex h-10 w-full items-center justify-center bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
				>
					Voltar
				</button>
		
		{:else if stepAtual == 3}
			<div
				class="flex h-80 w-full flex-col items-center justify-center gap-4 rounded-xl bg-white p-10 shadow-md"
			>
            </div>
				<button
					onclick={avancar}
					class="flex h-10 w-full items-center justify-center rounded border border-red-600 bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
				>
					Avançar
				</button>
				<button
					onclick={voltar}
					class="flex h-10 w-full items-center justify-center bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
				>
					Voltar
				</button>
			
		{/if}
	</div>
</div>
