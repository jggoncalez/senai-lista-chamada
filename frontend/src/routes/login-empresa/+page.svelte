<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { empresas as empresasApi } from '$lib/api';

  let empresasList = $state<string[]>([]);
  let empresaSelecionada = $state('');
  let password = $state('');
  let error = $state('');

  onMount(async () => {
    empresasList = await empresasApi.listar();
  });

  function handleLogin() {
    if (empresaSelecionada && password) {
      localStorage.setItem('company_logged_in', 'true');
      localStorage.setItem('company_name', empresaSelecionada);
      goto('/dashboard-empresa');
    } else {
      error = 'Por favor, preencha todos os campos.';
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50">
  <div class="bg-white rounded-2xl shadow-md p-10 w-full max-w-md flex flex-col items-center gap-6">
    
    <div class="flex flex-col items-center gap-2">
      <img src="/senai-logo.png" alt="senai logo" class="w-64">
      <h1 class="text-xl font-bold text-gray-800">Acesso Empresa</h1>
      <p class="text-gray-500">Controle de Frequência de Alunos</p>
    </div>

    <div class="w-full flex flex-col gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-sm font-semibold text-gray-600">Empresa</label>
        <select
          bind:value={empresaSelecionada}
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-red-500 bg-white"
        >
          <option value="">Selecione sua empresa...</option>
          {#each empresasList as emp}
            <option value={emp}>{emp}</option>
          {/each}
        </select>
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-semibold text-gray-600">Senha</label>
        <input
          type="password"
          bind:value={password}
          placeholder="••••••••"
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
      </div>

      {#if error}
        <p class="text-red-500 text-sm font-medium">{error}</p>
      {/if}

      <button
        onclick={handleLogin}
        class="w-full bg-red-600 text-white font-bold py-3 rounded-lg hover:bg-red-700 transition-colors shadow-md"
      >
        Entrar
      </button>

      <a href="/selecao" class="text-center text-sm text-gray-500 hover:text-gray-700 underline">
        Voltar para seleção
      </a>
    </div>
  </div>
</div>