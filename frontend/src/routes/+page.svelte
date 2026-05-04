
<script>

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