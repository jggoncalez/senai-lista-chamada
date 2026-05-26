<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { fade, fly } from 'svelte/transition';

	let { children } = $props();
	let companyName = $state('Empresa');

	onMount(() => {
		companyName = localStorage.getItem('company_name') || 'Empresa';
	});

	function handleLogout() {
		localStorage.removeItem('company_logged_in');
		localStorage.removeItem('company_name');
		goto('/selecao');
	}

    let activePath = $derived(page.url.pathname);
</script>

<div class="min-h-screen flex flex-col bg-gray-50">
	<!-- Navbar Empresa -->
	<nav class="bg-white border-b border-gray-200 px-6 h-16 flex items-center justify-between sticky top-0 z-20">
		<div class="flex items-center gap-3">
			<img src="/senai-logo.png" alt="SENAI" class="h-16">
			<span class="font-bold text-gray-700">{companyName}</span>
		</div>

  <div class="flex items-center gap-4">
    <div class="flex justify-center items-center gap-2 p-0 flex-row ">
    <button class="flex items-center gap-2  hover:bg-red-200 rounded-lg p-2" >
        <div class="flex p-4 h-5 w-5 items-center justify-center rounded-full bg-red-600 text-sm font-bold text-white ">
       
        </div>
        <span class="text-sm text-gray-500"></span>
        </button>
    </div>
    <a href="/login" aria-label="Fazer login" class="flex items-center no-underline hover:bg-red-200 rounded-lg p-2">
        <i><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M480-120v-80h280v-560H480v-80h280q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H480Zm-80-160-55-58 102-102H120v-80h327L345-622l55-58 200 200-200 200Z"/></svg></i> 
    </a>
  </div>
	</nav>

	<div class="flex flex-1 overflow-hidden ">
		<!-- Sidebar Empresa -->
		<aside class="bg-white w-64 border-r border-gray-200 flex flex-col p-5 gap-5 h-[calc(100vh-64px)]">
		        <a href="/login" class="bg-white border border-red-600 text-red-600 font-medium w-full h-10 flex items-center justify-center rounded hover:bg-red-600 hover:text-white transition-colors">
        <i><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#dc2626"><path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"/></svg></i>
        Voltar ao Início
        </a>
		<hr>
    <a href="/dashboard-empresa" class="flex flex-row w-full items-center gap-3 p-3 rounded-lg hover:bg-red-50 hover:text-red-600 transition-colors group">
        <i><svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#dc2626"><path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"/></svg></i>
        <div class="flex flex-col">
            <p class="font-bold text-md">Início</p>
            <p class="font-normal text-sm text-gray-500">Dashboard</p>
        </div>
    </a>
			
    <a href="/dashboard-empresa/relatorio" class="flex flex-row w-full items-center gap-3 p-3 rounded-lg hover:bg-red-50 hover:text-red-600 transition-colors group">
        <i><svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#dc2626"><path d="M320-453.33h320V-520H320v66.67Zm0 120h320V-400H320v66.67Zm0 120h200V-280H320v66.67ZM226.67-80q-27 0-46.84-19.83Q160-119.67 160-146.67v-666.66q0-27 19.83-46.84Q199.67-880 226.67-880H574l226 226v507.33q0 27-19.83 46.84Q760.33-80 733.33-80H226.67Zm314-542.67v-190.66h-314v666.66h506.66v-476H540.67Zm-314-190.66v190.66-190.66 666.66-666.66Z"/></svg></i>
        <div class="flex flex-col">
            <p class="font-bold text-md">Relatórios</p>
            <p class="font-normal text-sm text-gray-500">Ver Histórico</p>
        </div>
    </a>
		</aside>

		<!-- Main Content -->
		<main class="flex-1 overflow-y-auto p-8 bg-gray-50">
			<div in:fade={{ duration: 200 }}>
				{@render children()}
			</div>
		</main>
	</div>
</div>
