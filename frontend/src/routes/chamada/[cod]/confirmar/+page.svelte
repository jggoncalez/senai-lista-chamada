<script>
	import { page } from '$app/state';
    import CardConfirm  from '$lib/components/CardConfirm.svelte'
	let cod = page.params.cod ?? '3DEVT';
</script>

<!-- Breadcrumb -->
<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500">
	<a href="/dashboard" class="text-red-600 hover:underline">Dashboard</a>
	<span>›</span>
	<span class="text-gray-700">{cod}</span>
	<span>›</span>
	<span class="text-gray-700">Chamada</span>
	<span>›</span>
	<span class="text-red-600">Confirmar</span>
</nav>


<div class="flex w-full flex-1 items-center justify-center p-5 flex-col gap-3">
<h1 class="text-2xl font-bold">Confirmar Chamada</h1>
	<CardConfirm
        nomeTurma={"Desenvolvimento de Sistemas"}
        data={"20/04/2022"}
        diciplina={"Banco de Dados"}
        professor={"Samuel"}
        presentes={10}
        totalAlunos={20}
    />
      <!-- Botões com mesma largura do card -->
    <div class="flex w-full max-w-2xl items-center justify-between">
        <a 
            href="/chamada/{cod}"
            class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-800 transition-colors"
        >
            ‹ Voltar e Corrigir
        </a>
        <a
            href="/"
            class="bg-red-600 hover:bg-red-700 text-white font-medium px-6 py-2.5 rounded-xl transition-colors"
        >
            Salvar Chamada
        </a>
    </div>
    
</div>
