<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  // Mock data for the company dashboard
  let companyName = $state('');
  
  let students = [
    { id: 1, name: 'João Silva', turma: 'MEC-2024', frequency: 95, attendance: [true, true, true, false, true] },
    { id: 2, name: 'Maria Oliveira', turma: 'MEC-2024', frequency: 80, attendance: [true, false, true, true, false] },
    { id: 3, name: 'Pedro Santos', turma: 'MEC-2024', frequency: 100, attendance: [true, true, true, true, true] },
    { id: 4, name: 'Ana Costa', turma: 'ELE-2024', frequency: 60, attendance: [false, false, true, true, false] },
  ];

  let dates = ['19/05', '20/05', '21/05', '22/05', '23/05'];

  // onMount(() => {
  //   const loggedIn = localStorage.getItem('company_logged_in');
  //   if (!loggedIn) {
  //     goto('/login-empresa');
  //   }
  //   companyName = localStorage.getItem('company_name') || 'Empresa';
  // });

  function handleLogout() {
    localStorage.removeItem('company_logged_in');
    localStorage.removeItem('company_name');
    goto('/selecao');
  }
</script>

<div class="flex flex-col gap-6">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-bold text-gray-800">Resumo da Empresa</h1>
      <p class="text-gray-500">Acompanhamento geral de frequência</p>
    </div>
    
    <div class="flex gap-3">
      <button 
        onclick={() => goto('/dashboard-empresa/relatorio')}
        class="bg-white border border-red-600 text-red-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-50 flex items-center gap-2 shadow-sm"
      >
        Ver Relatório Detalhado
      </button>
    </div>
  </div>

  <!-- Stats -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <span class="text-sm text-gray-500 font-medium">Total de Alunos</span>
      <h2 class="text-3xl font-bold text-gray-800 mt-1">{students.length}</h2>
    </div>
    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <span class="text-sm text-gray-500 font-medium">Média de Frequência</span>
      <h2 class="text-3xl font-bold text-blue-600 mt-1">83.7%</h2>
    </div>
    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <span class="text-sm text-gray-500 font-medium">Alunos em Risco </span>
      <h2 class="text-3xl font-bold text-red-600 mt-1">1</h2>
    </div>
  </div>

  <!-- Table -->
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-left">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Aluno</th>
            <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase">Turma</th>
            {#each dates as date}
              <th class="px-3 py-4 text-xs font-bold text-gray-500 uppercase text-center">{date}</th>
            {/each}
            <th class="px-6 py-4 text-xs font-bold text-gray-500 uppercase text-right">Frequência</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          {#each students as student}
            <tr class="hover:bg-gray-50/50">
              <td class="px-6 py-4">
                <div class="font-medium text-gray-800">{student.name}</div>
              </td>
              <td class="px-6 py-4">
                <span class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">
                  {student.turma}
                </span>
              </td>
              {#each student.attendance as present}
                <td class="px-3 py-4 text-center">
                  {#if present}
                    <span class="text-green-600 font-bold">✓</span>
                  {:else}
                    <span class="text-red-500 font-bold">✕</span>
                  {/if}
                </td>
              {/each}
              <td class="px-6 py-4 text-right">
                <span class="font-bold {student.frequency >= 75 ? 'text-green-600' : 'text-red-600'}">
                  {student.frequency}%
                </span>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>