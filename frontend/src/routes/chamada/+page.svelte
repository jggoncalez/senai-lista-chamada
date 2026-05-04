<script lang="ts">
import CardTurma from "$lib/components/CardTurma.svelte";
const nomeTurmaMap: Record<string, string> = {
    '3DEVT': 'Desenvolvimento de Sistemas',
    '2ADM': 'Administração',
    '1DEVT': 'Desenvolvimento de Sistemas',
    '3ELET': 'Eletrotécnica',
    '2MEC': 'Mecânica'
};


let chamadas = $state([
		{ codTurma: '3DEVT', nomeAluno: 'Ana Maria Silva',       dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Amanda Nunes',          dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Beatriz Silva',         dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Bianca Pinheiro',       dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Bruno Araujo',          dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Carlos Camargo',        dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Daniel Luiz',           dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Edson Moraes',          dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Erico Baiano',          dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Fabricia Lima',         dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '3DEVT', nomeAluno: 'Gustavo Gonçalvez',     dataAula: '29/04/2026', disciplina: 'POO - Programação Orientada a Oração', presente: false },
		{ codTurma: '2ADM',  nomeAluno: 'Arthur Simas',          dataAula: '29/04/2026', disciplina: 'GER - Gestão de Robux',                presente: false },
		{ codTurma: '2ADM',  nomeAluno: 'Agatha Pereira',        dataAula: '29/04/2026', disciplina: 'GER - Gestão de Robux',                presente: false },
		{ codTurma: '2ADM',  nomeAluno: 'Bruno Arantes',         dataAula: '29/04/2026', disciplina: 'GER - Gestão de Robux',                presente: false },
		{ codTurma: '2ADM',  nomeAluno: 'Damião Costa',          dataAula: '29/04/2026', disciplina: 'GER - Gestão de Robux',                presente: false },
		{ codTurma: '1DEVT', nomeAluno: 'Ana Júlia Pereira',     dataAula: '29/04/2026', disciplina: 'LDL - Levantamento de Lego',           presente: false },
		{ codTurma: '1DEVT', nomeAluno: 'Ana Carolina Oliveira', dataAula: '29/04/2026', disciplina: 'LDL - Levantamento de Lego',           presente: false },
		{ codTurma: '3ELET', nomeAluno: 'Abner Silva',           dataAula: '29/04/2026', disciplina: 'CH - Tecnologia a Chuveirástica',      presente: false },
		{ codTurma: '3ELET', nomeAluno: 'Adão Marcos',           dataAula: '29/04/2026', disciplina: 'CH - Tecnologia a Chuveirástica',      presente: false },
		{ codTurma: '3ELET', nomeAluno: 'Bruno Moraes',          dataAula: '29/04/2026', disciplina: 'CH - Tecnologia a Chuveirástica',      presente: false },
		{ codTurma: '3ELET', nomeAluno: 'Caio Rodrigues',        dataAula: '29/04/2026', disciplina: 'CH - Tecnologia a Chuveirástica',      presente: false },
		{ codTurma: '3ELET', nomeAluno: 'Eymael Santos',         dataAula: '29/04/2026', disciplina: 'CH - Tecnologia a Chuveirástica',      presente: false },
		{ codTurma: '3ELET', nomeAluno: 'Humberto Golias',       dataAula: '29/04/2026', disciplina: 'CH - Tecnologia a Chuveirástica',      presente: false },
		{ codTurma: '2MEC',  nomeAluno: 'Platão Motta',          dataAula: '29/04/2026', disciplina: 'LPA - Lógica do Parafuso',             presente: false },
		{ codTurma: '2MEC',  nomeAluno: 'Ricardo Beckman',       dataAula: '29/04/2026', disciplina: 'LPA - Lógica do Parafuso',             presente: false },
		{ codTurma: '2MEC',  nomeAluno: 'Sarah Sena',            dataAula: '29/04/2026', disciplina: 'LPA - Lógica do Parafuso',             presente: false },
		{ codTurma: '2MEC',  nomeAluno: 'Thiago Mota',           dataAula: '29/04/2026', disciplina: 'LPA - Lógica do Parafuso',             presente: false },
		{ codTurma: '2MEC',  nomeAluno: 'Welington Silva',       dataAula: '29/04/2026', disciplina: 'LPA - Lógica do Parafuso',             presente: false }
	]);
  let codturmas = $derived([...new Set(chamadas.map((c)=> c.codTurma))])
</script>
<div class="p-4 gap-3 flex flex-col">
  <h1 class="text-xl font-bold text-gray-800">Turmas Disponíveis</h1>
<div class="flex flex-row gap-5 w-full items-left justify-between">
  {#each codturmas as t }
  <CardTurma
    codTurma={codturmas[0]}
    nomeTurma={nomeTurmaMap[t]}
    totalAlunos={chamadas.filter((c) => c.codTurma === t ).length}
  />
{/each}
</div>
</div>

