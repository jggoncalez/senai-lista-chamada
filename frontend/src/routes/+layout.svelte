<script lang="ts">
  import './layout.css';
  import favicon from '$lib/assets/favicon.ico';
  import Navbar from '$lib/components/Navbar.svelte';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import Acessiblidade from '$lib/components/acessiblidade.svelte';
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  // Importando os efeitos de transição do Svelte
  import { fade, fly } from 'svelte/transition';

  let isPublicPage = $derived(['/login', '/login-empresa', '/selecao', '/dashboard-empresa'].includes(page.url.pathname));
  let { children } = $props();

  onMount(() => {
    if (page.url.pathname === '/') {
      goto('/selecao');
    }
  });
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<Acessiblidade />

{#if isPublicPage}
  <div in:fade={{ duration: 300 }}>
    {@render children()}
  </div>
{:else}
  <div class="min-h-screen flex flex-col bg-gray-50 transition-colors duration-300">
    
    <div in:fly={{ y: -20, duration: 400 }}>
      <Navbar />
    </div>

    <div class="flex flex-1 overflow-hidden">
      <div in:fly={{ x: -40, duration: 400, delay: 100 }}>
        <Sidebar />
      </div>
        <main 
          class="flex-1 p-8 bg-gray-50 text-gray-900  transition-colors duration-300"
          in:fly={{ y: 15, duration: 350, delay: 200 }}
          out:fade={{ duration: 150 }}
        >
          {@render children()}
        </main>
    </div>
  </div>
{/if}