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

<div class="min-h-screen bg-gray-50 flex flex-col">
  <!-- Top Bar -->
  <header class="bg-white border-b border-gray-200 px-8 h-16 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <img src="/senai-logo.png" alt="SENAI" class="h-10">
      <div class="h-6 w-px bg-gray-300"></div>
      <span class="font-bold text-gray-700">{companyName}</span>
    </div>
    <button 
      onclick={handleLogout}
      class="text-sm font-medium text-red-600 hover:text-red-700 flex items-center gap-2"
    >
      <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="currentColor">
        <path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h280v80H200Zm440-160-55-58 102-102H360v-80h327L585-622l55-58 200 200-200 200Z"/>
      </svg>
      Sair
    </button>
  </header>

  <!-- Main Content -->
  <main class="p-8 flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Dashboard de Alunos</h1>
        <p class="text-gray-500">Acompanhamento de frequência dos alunos vinculados</p>
      </div>
      
      <div class="flex gap-3">
        <button class="bg-white border border-gray-300 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 flex items-center gap-2 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 -960 960 960" width="18px" fill="currentColor">
            <path d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/>
          </svg>
          PDF
        </button>
        <button class="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 flex items-center gap-2 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 -960 960 960" width="18px" fill="currentColor">
            <path d="M440-120v-480H120v-160q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H440Zm80-80h240v-160H520v160Zm0-240h240v-160H520v160ZM200-680h560v-80H200v80Z"/>
          </svg>
          Excel
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
  </main>
</div>