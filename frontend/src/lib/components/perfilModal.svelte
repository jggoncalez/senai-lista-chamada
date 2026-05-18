<script lang="ts">
  import { onMount } from 'svelte';
  import { usuario, type ProfessorResponse } from '$lib/api';

  let { status, onclose } = $props();

  let user = $state<ProfessorResponse | null>(null);

  onMount(async () => {
    user = await usuario.buscar();
  });

  // Pega as iniciais do nome
  let iniciais = $derived(
    user?.nome
      ? user.nome.split(' ').slice(0, 2).map((n) => n[0]).join('').toUpperCase()
      : '?'
  );
</script>

{#if status}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
  >
    <div
      class="relative w-full max-w-sm rounded-2xl bg-white shadow-xl"

    >
      <button
        onclick={onclose}
        class="absolute right-4 top-4 text-gray-200 hover:text-gray-600 transition-colors"
        aria-label="Fechar"
      >
        ✕
      </button>

      <div class="flex flex-col items-center rounded-t-2xl bg-red-600 px-6 pb-6 pt-8">
        <div class="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-white text-2xl font-bold text-slate-800">
          {iniciais}
        </div>
        <h2 class="text-xl font-bold text-white">{user?.nome ?? '...'}</h2>
        <p class="text-sm text-gray-200">
          {user?.roles?.includes('admin') ? 'Administrador' : 'Professor(a)'}
        </p>
      </div>

      <div class="flex flex-col gap-3 p-6">
        <div class="flex items-center gap-3 rounded-lg bg-gray-50 px-4 py-3">
          <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280">
            <path d="M160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720v480q0 33-23.5 56.5T800-160H160Zm320-280L160-640v400h640v-400L480-440Zm0-80 320-200H160l320 200ZM160-640v-80 480-400Z"/>
          </svg>
          <div class="flex flex-col">
            <span class="text-xs text-gray-400">Email Institucional</span>
            <span class="text-sm font-medium text-gray-800">{user?.email ?? '...'}</span>
          </div>
        </div>

        <div class="flex items-center gap-3 rounded-lg bg-gray-50 px-4 py-3">
          <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280">
            <path d="M480-440q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0-80q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0 440q-139-35-229.5-159.5T160-516v-244l320-120 320 120v244q0 152-90.5 276.5T480-80Z"/>
          </svg>
          <div class="flex flex-col">
            <span class="text-xs text-gray-400">Perfil de Acesso</span>
            <span class="text-sm font-medium text-gray-800">
              {user?.roles?.join(', ') ?? '...'}
            </span>
          </div>
        </div>
      </div>

      <div class="px-6 pb-6">
        <button
          onclick={onclose}
          class="w-full rounded-xl bg-red-600 py-3 font-medium text-white transition-colors hover:bg-red-700"
        >
          Fechar
        </button>
      </div>
    </div>
  </div>
{/if}