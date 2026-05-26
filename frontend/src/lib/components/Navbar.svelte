<script lang="ts">
  import { onMount } from 'svelte';
  import { usuario, type ProfessorResponse } from '$lib/api';
  import PerfilModal from './perfilModal.svelte';
  let status = $state(false);
  let User = $state<ProfessorResponse | null>(null);

  onMount(async () => {
    User = await usuario.buscar();
  });

    let iniciais = $derived(
    User?.nome
      ? User.nome.split(' ').slice(0, 2).map((n) => n[0]).join('').toUpperCase()
      : '?'
  );
</script>
<nav class="bg-white border-b border-gray-200 px-6 h-16 flex items-center justify-between sticky top-0">
  
  <div class="flex items-center gap-3">
    <img src="/senai-logo.png" alt="SENAI" class="h-20">
    <span class="font-semibold text-gray-800">Sistema de Chamada</span>
  </div>

  <div class="flex items-center gap-4">
    <div class="flex justify-center items-center gap-2 p-0 flex-row ">
    <button class="flex items-center gap-2  hover:bg-red-200 rounded-lg p-2" onclick={()=>{status = !status}}>
        <div class="flex p-4 h-5 w-5 items-center justify-center rounded-full bg-red-600 text-sm font-bold text-white ">
          {iniciais}
        </div>
        <span class="text-sm text-gray-500">{User?.nome}</span>
        </button>
    </div>
    <a href="/login" aria-label="Fazer login" class="flex items-center no-underline hover:bg-red-200 rounded-lg p-2">
        <i><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M480-120v-80h280v-560H480v-80h280q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H480Zm-80-160-55-58 102-102H120v-80h327L345-622l55-58 200 200-200 200Z"/></svg></i> 
    </a>
  </div>
</nav>
<PerfilModal status={status} onclose={() => status = false} />