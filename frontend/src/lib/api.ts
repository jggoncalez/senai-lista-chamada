const BASE = 'http://localhost:8000';

export interface ChamadaCreate {
  nome_aluno: string;
  cod_turma: string;
  data_aula: string;
  disciplina: string;
  presente: boolean;
}

export interface AlunoResponse {
  id: number;
  nome: string;
  turma: string;
  cod_turma: string;
  chamada: number | null;
}

export interface ChamadaItem {
  id: number | null;
  nome_aluno: string;
  cod_turma: string;
  data_aula: string;
  disciplina: string;
  presente: boolean;
}

export interface TurmaItem {
  cod: string;
  nome: string;
  totalAlunos: number;
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  });
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  return res.json();
}

export const alunos = {
  listar: () => apiFetch('/alunos') as Promise<AlunoResponse[]>,
  porTurma: (cod: string) => apiFetch(`/alunos?turma=${cod}`) as Promise<AlunoResponse[]>
};

export const turmas = {
  listar: async (): Promise<TurmaItem[]> => {
    const todos: AlunoResponse[] = await alunos.listar();
    const map = new Map<string, TurmaItem>();
    for (const a of todos) {
      if (!map.has(a.cod_turma)) {
        map.set(a.cod_turma, { cod: a.cod_turma, nome: a.turma, totalAlunos: 0 });
      }
      map.get(a.cod_turma)!.totalAlunos++;
    }
    return [...map.values()];
  }
};

export const chamadas = {
  registrar: (dados: ChamadaCreate) =>
    apiFetch('/chamadas', { method: 'POST', body: JSON.stringify(dados) }),

  relatorio: (turma: string, data: string) =>
    apiFetch(`/chamadas/relatorio?turma=${turma}&data=${data}`),

  listarPorTurma: (turma: string, data = ''): Promise<ChamadaItem[]> =>
    apiFetch(`/chamadas/relatorio?turma=${encodeURIComponent(turma)}&data=${encodeURIComponent(data)}`),

  atualizar: (id: number, presente: boolean) =>
    apiFetch(`/chamadas/${id}`, { method: 'PATCH', body: JSON.stringify({ presente }) })
};
