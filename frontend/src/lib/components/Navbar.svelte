<!-- src/lib/components/Navbar.svelte -->
<!-- <script>
  import { usuario } from "$lib/stores/auth";
</script> -->

<nav class="bg-white border-b border-gray-200 px-6 h-16 flex items-center justify-between">
  
  <div class="flex items-center gap-3">
    <img src="/senai-logo.png" alt="SENAI" class="h-20">
    <span class="font-semibold text-gray-800">Sistema de Chamada</span>
  </div>

  <div class="flex items-center gap-4">
    <div class="flex justify-center items-center gap-2 p-0 flex-row ">
        <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#000000"><path d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm146.5-204.5Q340-521 340-580t40.5-99.5Q421-720 480-720t99.5 40.5Q620-639 620-580t-40.5 99.5Q539-440 480-440t-99.5-40.5ZM480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm100-95.5q47-15.5 86-44.5-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160q53 0 100-15.5ZM523-537q17-17 17-43t-17-43q-17-17-43-17t-43 17q-17 17-17 43t17 43q17 17 43 17t43-17Zm-43-43Zm0 360Z"/></svg>
        <span class="text-sm text-gray-500"><!--{$usuario?.nome}  --> Morsa</span>
    </div>
    <a href="/login" aria-label="Fazer login" class="flex items-center no-underline">
        <i><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M480-120v-80h280v-560H480v-80h280q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H480Zm-80-160-55-58 102-102H120v-80h327L345-622l55-58 200 200-200 200Z"/></svg></i> 
    </a>
  </div>

</nav>
