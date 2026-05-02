<script> 
let Logado = false;
let nome = "morsa"

</script>
    <div class="min-h-screen flex items-center justify-center">
        <div class="bg-white rounded-2xl shadow-lg p-10 w-full max-w-md">
            {#if Logado}
                <h1>Olá, {nome}</h1>
                <p>Bem Vindo</p>
            {:else}
                <a href="/login" class="w-full flex items-center justify-center gap-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl transition-colors">Entrar</a>
            {/if}
        </div>
    </div>
