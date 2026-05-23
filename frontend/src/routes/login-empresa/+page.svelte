<script lang="ts">
  import { goto } from '$app/navigation';
  
  let cnpj = $state('');
  let password = $state('');
  let error = $state('');

  function handleLogin() {
    if (cnpj && password) {
      localStorage.setItem('company_logged_in', 'true');
      localStorage.setItem('company_name', 'Empresa Exemplo S/A');
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

    <form class="w-full flex flex-col gap-4" onsubmit={(e) => { e.preventDefault(); handleLogin(); }}>
      <div class="flex flex-col gap-1">
        <label for="cnpj" class="text-sm font-semibold text-gray-600">CNPJ</label>
        <input 
          type="text" 
          id="cnpj"
          bind:value={cnpj}
          placeholder="00.000.000/0000-00"
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>

      <div class="flex flex-col gap-1">
        <label for="password" class="text-sm font-semibold text-gray-600">Senha</label>
        <input 
          type="password" 
          id="password"
          bind:value={password}
          placeholder="••••••••"
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>

      {#if error}
        <p class="text-red-500 text-sm font-medium">{error}</p>
      {/if}

      <button 
        type="submit"
        class="w-full bg-red-600 text-white font-bold py-3 rounded-lg hover:bg-red-700 transition-colors shadow-md"
      >
        Entrar
      </button>

      <a href="/selecao" class="text-center text-sm text-gray-500 hover:text-gray-700 underline">
        Voltar para seleção
      </a>
    </form>

  </div>
</div>