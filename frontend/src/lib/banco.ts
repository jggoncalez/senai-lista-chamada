
interface Aluno {
_F_NOME    : string;
_F_TURMA   : string;
_F_COD     : string;
_F_CHAMADA : number;
}

import { apiFetch } from '$lib/api';

export  const nomeTurmaMap: Record<string, string> = {
        '3DEVT': 'Desenvolvimento de Sistemas',
        '2ADM': 'Administração',
        '1DEVT': 'Desenvolvimento de Sistemas',
        '3ELET': 'Eletrotécnica',
        '2MEC': 'Mecânica'
    };
export   const disciplinasMap: Record<string, string[]> = {
        '3DEVT': ['POO - Programação Orientada a Objetos', 'BD - Banco de Dados'],
        '2ADM': ['GER - Gestão Empresarial', 'MKT - Marketing'],
        '1DEVT': ['LDL - Lógica de Programação'],
        '3ELET': ['CH - Circuitos Elétricos'],
        '2MEC': ['LPA - Lógica do Parafuso']
    };



export const chamadas = $state({
  dados: [] as Aluno[],
  async carregar() {
    this.dados = await  apiFetch('/alunos');
  }
});





