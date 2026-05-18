<script lang="ts">
  import './layout.css';
  import favicon from '$lib/assets/favicon.ico';
  import Navbar from '$lib/components/Navbar.svelte';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import { page } from '$app/state';
  let isLogin = $derived(page.url.pathname === '/login');
  let { children } = $props();

  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  onMount(() => {
    goto('/login');
  });
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

{#if isLogin}
  {@render children()}
{:else}
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <div class="flex flex-1">
      <Sidebar />
      <main class="flex-1 p-8 bg-gray-50">
        {@render children()}
        
      </main>
    </div>
  </div>
{/if}