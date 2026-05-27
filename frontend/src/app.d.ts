declare global {
  namespace App {
    interface PageState {
      nomeTurma?: string;
      dataAula?: string;
      disciplinaId?: number | null;
      disciplinaNome?: string;
      presencaMap?: Record<number, boolean>;
      listaAlunos?: Array<{
        id: number;
        nome: string;
        turma: string;
        cod_turma: string;
        chamada: number | null;
      }>;
      professorId?: number | null;  // ← adicione
    }
  }
}

export {};