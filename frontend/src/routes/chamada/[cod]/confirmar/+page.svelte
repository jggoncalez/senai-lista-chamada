<script>
    import { page } from '$app/state';
    import { goto } from '$app/navigation';
    import CardConfirm from '$lib/components/CardConfirm.svelte';
    import { chamadas as chamadasApi } from '$lib/api';

    // 1. Buscamos do page.state (onde o goto salvou) e não do page.data
    // Usamos valores padrão (??) para evitar que o componente quebre se estiver vazio
    /** @type {any} */
    const pageState = page.state;
    let nomeTurma = $derived(pageState.nomeTurma ?? 'Não informada');
    let dataAula = $derived(pageState.dataAula ?? '');
    let disciplinaSelecionada = $derived(pageState.disciplinaSelecionada ?? 'Não informada');
    let presencaMap = $derived(pageState.presencaMap ?? {});
    let listaAlunos = $derived(pageState.listaAlunos ?? []);
    
    // 2. Total de alunos baseado na lista que veio do state
    let totalAlunos = $derived(listaAlunos.length);
    // Conta quantos alunos têm valor 'true' no mapa de presença
    let totalPresentes = $derived(
        Object.values(presencaMap).filter(p => p === true).length
    );
    // 3. O nome do professor geralmente vem do Layout (page.data)
    let nomeProfessor = $derived(page.data.user?.nome || 'Visitante');
    
    let cod = page.params.cod ?? '3DEVT';

    async function salvarChamada() {
        // Agora usamos a listaAlunos que veio do state
        for (const aluno of listaAlunos) {
            await chamadasApi.registrar({
                nome_aluno: aluno.nome,
                cod_turma: cod,
                data_aula: dataAula,
                disciplina: disciplinaSelecionada,
                presente: presencaMap[aluno.nome] ?? true
            });
        }
        goto('/'); 
    }
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
        nomeTurma={nomeTurma}
        data={dataAula}
        diciplina={disciplinaSelecionada}
        professor={nomeProfessor}
        presentes={totalPresentes}
        totalAlunos={totalAlunos}
    />
      <!-- Botões com mesma largura do card -->
    <div class="flex w-full max-w-2xl items-center justify-between">
        <a 
            href="/chamada/{cod}"
            class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-800 transition-colors"
        >
            ‹ Voltar e Corrigir
        </a>
        <button
            onclick={salvarChamada}
            class="bg-red-600 hover:bg-red-700 text-white font-medium px-6 py-2.5 rounded-xl transition-colors"
        >
            Salvar Chamada
    </button>
    </div>
    
</div>
