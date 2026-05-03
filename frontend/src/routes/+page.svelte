
<script>
  // import { onMount } from "svelte";
  // import { goto } from "$app/navigation";
  // import { isLogado } from "$lib/stores/auth";
  // import { get } from "svelte/store";

  // onMount(() => {
  //   if (get(isLogado)) {
  //     goto("/dashboard");
  //   } else {
  //     goto("/login");
  //   }
  // });
  import CardTurma from "$lib/components/CardTurma.svelte";
let turmas = [
  { codTurma: "3DEVT", nome: "Desenvolvimento de Sistemas", total: 32 },
  { codTurma: "3ELET", nome: "Eletroeletrônica", total: 25 },
];
</script>

{#each turmas as t (t.codTurma)}
  <CardTurma
    codTurma={t.codTurma}
    nomeTurma={t.nome}
    totalAlunos={t.total}
  />
{/each}