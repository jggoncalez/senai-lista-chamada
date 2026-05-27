<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { chamadas as chamadasApi } from '$lib/api';
  import type { ChamadaItem } from '$lib/api';

  let companyName = $state('');
  let chamadaEmpresa = $state<ChamadaItem[]>([]);
  let carregando = $state(true);

  onMount(async () => {
    const loggedIn = localStorage.getItem('company_logged_in');
    if (!loggedIn) {
      goto('/login-empresa');
      return;
    }
    companyName = localStorage.getItem('company_name') || '';
    try {
      chamadaEmpresa = await chamadasApi.listarPorEmpresa(companyName);
    } catch (e) {
      console.error(e);
    } finally {
      carregando = false;
    }
  });

  let alunosUnicos = $derived([...new Set(chamadaEmpresa.map(c => c.nome_aluno))]);
  let totalRegistros = $derived(chamadaEmpresa.length);
  let totalPresentes = $derived(chamadaEmpresa.filter(c => c.presente).length);
  let frequenciaMedia = $derived(
    totalRegistros ? Math.round((totalPresentes / totalRegistros) * 100) : 0
  );
  let alunosRisco = $derived(
    alunosUnicos.filter(nome => {
      const registros = chamadaEmpresa.filter(c => c.nome_aluno === nome);
      if (!registros.length) return false;
      const pct = (registros.filter(c => c.presente).length / registros.length) * 100;
      return pct < 75;
    })
  );

  // Últimas datas com chamada
  let ultimasDatas = $derived(
    [...new Set(chamadaEmpresa.map(c => c.data_aula.slice(0, 10)))].sort().slice(-5)
  );

  function getPresenca(nome: string, data: string): boolean | null {
    const r = chamadaEmpresa.find(c => c.nome_aluno === nome && c.data_aula.slice(0, 10) === data);
    return r ? r.presente : null;
  }

  function getFrequencia(nome: string): number {
    const registros = chamadaEmpresa.filter(c => c.nome_aluno === nome);
    if (!registros.length) return 0;
    return Math.round((registros.filter(c => c.presente).length / registros.length) * 100);
  }
</script>

<div class="flex flex-col gap-6">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-bold text-gray-800">Resumo — {companyName}</h1>
      <p class="text-gray-500">Acompanhamento geral de frequência</p>
    </div>
    <button
      onclick={() => goto('/dashboard-empresa/relatorio')}
      class="bg-white border border-red-600 text-red-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-50 flex items-center gap-2 shadow-sm"
    >
      Ver Relatório Detalhado
    </button>
  </div>

  {#if carregando}
    <div class="flex items-center justify-center py-20 text-gray-400">Carregando...</div>
  {:else}
    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <span class="text-sm text-gray-500 font-medium">Total de Alunos</span>
        <h2 class="text-3xl font-bold text-gray-800 mt-1">{alunosUnicos.length}</h2>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <span class="text-sm text-gray-500 font-medium">Frequência Média</span>
        <h2 class="text-3xl font-bold text-blue-600 mt-1">{frequenciaMedia}%</h2>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <span class="text-sm text-gray-500 font-medium">Alunos em Risco (&lt;75%)</span>
        <h2 class="text-3xl font-bold text-red-600 mt-1">{alunosRisco.length}</h2>
      </div>
    </div>

    <!-- Tabela resumo -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="p-5 border-b border-gray-100 flex justify-between items-center">
        <h3 class="font-bold text-gray-700">Frequência por Aluno</h3>
        <span class="text-xs text-gray-400">{alunosUnicos.length} alunos vinculados</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Aluno</th>
              <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Turma</th>
              {#each ultimasDatas as data}
                <th class="px-3 py-4 text-xs font-bold text-gray-500 uppercase text-center">
                  {data.slice(8)}/{data.slice(5,7)}
                </th>
              {/each}
              <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase text-right">Frequência</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            {#each alunosUnicos as nome}
              {@const freq = getFrequencia(nome)}
              {@const turma = chamadaEmpresa.find(c => c.nome_aluno === nome)?.cod_turma ?? '—'}
              <tr class="hover:bg-gray-50/50">
                <td class="px-6 py-4 font-medium text-gray-800">{nome}</td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">{turma}</span>
                </td>
                {#each ultimasDatas as data}
                  {@const p = getPresenca(nome, data)}
                  <td class="px-3 py-4 text-center">
                    {#if p === true}
                      <span class="text-green-600 font-bold">✓</span>
                    {:else if p === false}
                      <span class="text-red-500 font-bold">✕</span>
                    {:else}
                      <span class="text-gray-300">—</span>
                    {/if}
                  </td>
                {/each}
                <td class="px-6 py-4 text-right font-bold {freq >= 75 ? 'text-green-600' : 'text-red-600'}">
                  {freq}%
                </td>
              </tr>
            {/each}

            {#if alunosUnicos.length === 0}
              <tr>
                <td colspan="99" class="px-6 py-12 text-center text-sm text-gray-400">
                  Nenhum aluno vinculado a esta empresa ainda.
                </td>
              </tr>
            {/if}
          </tbody>
        </table>
      </div>
    </div>
  {/if}
</div>