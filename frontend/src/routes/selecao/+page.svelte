<div class="min-h-screen flex items-center justify-center bg-gray-50">
  <div class="bg-white rounded-2xl shadow-md p-10 w-full max-w-2xl flex flex-col items-center gap-8">
    
    <div class="flex flex-col items-center gap-2">
      <img src="/senai-logo.png" alt="senai logo" class="w-64">
      <h1 class="text-2xl font-bold text-gray-800">Sistema de Chamada</h1>
      <p class="text-gray-500">Selecione seu tipo de acesso</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
      <!-- Opção SENAI -->
      <a href="/login" class="group flex flex-col items-center gap-4 p-8 border-2 border-transparent hover:border-red-600 rounded-2xl bg-gray-50 transition-all">
        <div class="w-16 h-16 rounded-full bg-red-100 flex items-center justify-center text-red-600 group-hover:bg-red-600 group-hover:text-white transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" height="32px" viewBox="0 -960 960 960" width="32px" fill="currentColor">
            <path d="M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-240v-80q0-33 17-61t47-45q67-30 132-42t124-12q59 0 124 12t132 42q30 17 47 45t17 61v80H160Z"/>
          </svg>
        </div>
        <div class="text-center">
          <h2 class="text-lg font-bold text-gray-800">Sou Colaborador</h2>
          <p class="text-sm text-gray-500 mt-1">Acesso para professores e administradores SENAI</p>
        </div>
      </a>

      <!-- Opção Empresa -->
      <a href="/login-empresa" class="group flex flex-col items-center gap-4 p-8 border-2 border-transparent hover:border-blue-600 rounded-2xl bg-gray-50 transition-all">
        <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" height="32px" viewBox="0 -960 960 960" width="32px" fill="currentColor">
            <path d="M120-120v-560h160v-160h400v320h160v400H120Zm80-80h80v-80h-80v80Zm0-160h80v-80h-80v80Zm0-160h80v-80h-80v80Zm240 320h80v-80h-80v80Zm0-160h80v-80h-80v80Zm0-160h80v-80h-80v80Zm0-160h80v-80h-80v80Zm240 480h80v-80h-80v80Zm0-160h80v-80h-80v80Z"/>
          </svg>
        </div>
        <div class="text-center">
          <h2 class="text-lg font-bold text-gray-800">Sou Empresa</h2>
          <p class="text-sm text-gray-500 mt-1">Acompanhe a frequência dos seus alunos</p>
        </div>
      </a>
    </div>

  </div>
</div>