<script lang="ts">
  import './layout.css';
  import favicon from '$lib/assets/favicon.ico';
  import Navbar from '$lib/components/Navbar.svelte';
  import Sidebar from '$lib/components/Sidebar.svelte';

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<div class="min-h-screen flex flex-col">
  <Navbar />

  <div class="flex flex-1">
    <Sidebar />
    <main class="flex-1 p-8 bg-gray-50">
      {@render children()}
    </main>
  </div>
</div>