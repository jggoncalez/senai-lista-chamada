const BASE = 'http://localhost:8000';

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
  chamada?: number | null;
  data_aula: string;
  disciplina: string;
  presente: boolean;
}

export interface TurmaItem {
  cod: string;
  nome: string;
  totalAlunos: number;
}

export interface TurmaDisciplinaItem {
  id: number;
  turma_id: number;
  curso_id: number;
  professor_id: number | null;
  dia_semana: number | null;
  ativo: boolean;
}

export interface SessaoItem {
  id: number;
  turma_disciplina_id: number;
  professor_id: number;
  data_aula: string;
  observacao: string | null;
}

export interface ProfessorResponse {
  id: number | null;
  nome: string;
  email: string;
  roles: string[];
}

export interface CursoItem {
  id: number;
  nome: string;
  carga_horaria: number;
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => '');
    throw new Error(`Erro ${res.status}: ${detail}`);
  }
  return res.json();
}

export const usuario = {
  buscar: () => apiFetch('/auth/me') as Promise<ProfessorResponse>,
};

export const alunos = {
  listar: () => apiFetch('/alunos') as Promise<AlunoResponse[]>,
  porTurma: (cod: string) => apiFetch(`/alunos?turma=${cod}`) as Promise<AlunoResponse[]>,
  importarLote: (dados: unknown[]) =>
    apiFetch('/alunos/import/batch', { method: 'POST', body: JSON.stringify(dados) }),
};

export const cursos = {
  listar: () => apiFetch('/cursos') as Promise<CursoItem[]>,
};

export const turmas = {
  listar: async (): Promise<TurmaItem[]> => {
    const todos: AlunoResponse[] = await alunos.listar();
    const map = new Map<string, { nomes: Set<string>; nome: string }>();
    for (const a of todos) {
      if (!map.has(a.cod_turma)) {
        map.set(a.cod_turma, { nomes: new Set(), nome: a.turma });
      }
      map.get(a.cod_turma)!.nomes.add(a.nome);
    }
    return [...map.entries()].map(([cod, data]) => ({
      cod,
      nome: data.nome,
      totalAlunos: data.nomes.size,
    }));
  },
};

export const turmaDisciplinas = {
  porTurma: (turmaId: number) =>
    apiFetch(`/turma-disciplinas?turma_id=${turmaId}`) as Promise<TurmaDisciplinaItem[]>,
  hoje: () => apiFetch('/turma-disciplinas/hoje') as Promise<TurmaDisciplinaItem[]>,
};

export const sessoes = {
  // Busca ou cria sessão para uma turma-disciplina + data
  criarOuBuscar: (dados: {
    turma_disciplina_id: number;
    professor_id?: number | null;
    data_aula: string;
  }) => apiFetch('/sessoes', { method: 'POST', body: JSON.stringify(dados) }) as Promise<SessaoItem>,
};
export const empresas = {
    listar: (): Promise<string[]> =>
        apiFetch('/alunos').then((alunos: AlunoResponse[]) =>
            [...new Set(alunos.map((a: any) => a.empresa).filter(Boolean))].sort()
        ),
};

export const chamadas = {
  // Salva chamada completa (fluxo novo: sessão → lote)
  salvarLote: async (
    sessaoId: number,
    presencas: Array<{ aluno_id: number; presente: boolean }>
  ) =>
    apiFetch('/chamadas/lote', {
      method: 'POST',
      body: JSON.stringify({ sessao_id: sessaoId, presencas }),
    }),

  // Relatório por turma com filtro de datas
  listarPorTurma: (turma: string, dataInicio = '', dataFim = ''): Promise<ChamadaItem[]> => {
    const params = new URLSearchParams({ turma });
    if (dataInicio) params.set('data_inicio', dataInicio);
    if (dataFim) params.set('data_fim', dataFim);
    return apiFetch(`/chamadas/relatorio?${params}`);
  },

  // Relatório por empresa
listarPorEmpresa: (empresa: string, dataInicio = '', dataFim = ''): Promise<ChamadaItem[]> => {
    const params = new URLSearchParams({ empresa });
    if (dataInicio) params.set('data_inicio', dataInicio);
    if (dataFim) params.set('data_fim', dataFim);
    return apiFetch(`/chamadas/relatorio?${params}`);
},


  atualizar: (id: number, presente: boolean) =>
    apiFetch(`/chamadas/${id}`, { method: 'PATCH', body: JSON.stringify({ presente }) }),
};