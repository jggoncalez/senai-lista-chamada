<script lang="ts">
    import { page } from '$app/state';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';

    let { children } = $props();
    let companyName = $state('');

    onMount(() => {
        const loggedIn = localStorage.getItem('company_logged_in');
        if (!loggedIn) {
            goto('/login-empresa');
            return;
        }
        companyName = localStorage.getItem('company_name') || 'Empresa';
    });

    function handleLogout() {
        localStorage.removeItem('company_logged_in');
        localStorage.removeItem('company_name');
        goto('/selecao');
    }
</script>

<div class="flex h-screen flex-col bg-gray-50">
	<!-- Navbar Empresa -->
	<nav
		class="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6"
	>
		<div class="flex items-center gap-3">
			<img src="/senai-logo.png" alt="SENAI" class="h-16" />
			<span class="font-bold text-gray-700">{companyName}</span>
		</div>

<div class="flex items-center gap-4">
    <div class="flex justify-center items-center gap-2 p-0 flex-row">
        <div class="flex items-center gap-2 hover:bg-red-200 rounded-lg p-2">
            <div class="flex p-4 h-5 w-5 items-center justify-center rounded-full bg-red-600 text-sm font-bold text-white">
                {companyName ? companyName[0].toUpperCase() : 'E'}
            </div>
            <span class="text-sm text-gray-500">{companyName}</span>
        </div>
    </div>
    <button
        onclick={handleLogout}
        aria-label="Sair"
        class="flex items-center no-underline hover:bg-red-200 rounded-lg p-2"
    >
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000">
            <path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h280v80H200Zm440-160-55-58 102-102H360v-80h327L585-622l55-58 200 200-200 200Z"/>
        </svg>
    </button>
</div>
	</nav>

	<div class="flex flex-1 overflow-hidden min-h-0">
		<!-- Sidebar Empresa -->
		<aside
			class="flex h-full w-64 flex-col gap-5 border-r border-gray-200 bg-white p-5"
		>
			<a
				href="/login"
				class="flex h-10 w-full items-center justify-center rounded border border-red-600 bg-white font-medium text-red-600 transition-colors hover:bg-red-600 hover:text-white"
			>
				<i
					><svg
						xmlns="http://www.w3.org/2000/svg"
						height="24px"
						viewBox="0 -960 960 960"
						width="24px"
						fill="#dc2626"
						><path
							d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"
						/></svg
					></i
				>
				Voltar ao Início
			</a>
			<hr />
			<a
				href="/dashboard-empresa"
				class="group flex w-full flex-row items-center gap-3 rounded-lg p-3 transition-colors hover:bg-red-50 hover:text-red-600"
			>
				<i
					><svg
						xmlns="http://www.w3.org/2000/svg"
						height="40px"
						viewBox="0 -960 960 960"
						width="40px"
						fill="#dc2626"
						><path
							d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"
						/></svg
					></i
				>
				<div class="flex flex-col">
					<p class="text-md font-bold">Início</p>
					<p class="text-sm font-normal text-gray-500">Dashboard</p>
				</div>
			</a>

			<a
				href="/dashboard-empresa/relatorio"
				class="group flex w-full flex-row items-center gap-3 rounded-lg p-3 transition-colors hover:bg-red-50 hover:text-red-600"
			>
				<i
					><svg
						xmlns="http://www.w3.org/2000/svg"
						height="40px"
						viewBox="0 -960 960 960"
						width="40px"
						fill="#dc2626"
						><path
							d="M320-453.33h320V-520H320v66.67Zm0 120h320V-400H320v66.67Zm0 120h200V-280H320v66.67ZM226.67-80q-27 0-46.84-19.83Q160-119.67 160-146.67v-666.66q0-27 19.83-46.84Q199.67-880 226.67-880H574l226 226v507.33q0 27-19.83 46.84Q760.33-80 733.33-80H226.67Zm314-542.67v-190.66h-314v666.66h506.66v-476H540.67Zm-314-190.66v190.66-190.66 666.66-666.66Z"
						/></svg
					></i
				>
				<div class="flex flex-col">
					<p class="text-md font-bold">Relatórios</p>
					<p class="text-sm font-normal text-gray-500">Ver Histórico</p>
				</div>
			</a>
		</aside>

		<!-- Main Content -->
		<main class="flex-1 overflow-y-auto bg-gray-50 p-8">
			<div in:fade={{ duration: 200 }}>
				{@render children()}
			</div>
		</main>
	</div>
</div>
