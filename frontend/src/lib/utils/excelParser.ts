import * as XLSX from 'xlsx';

export interface ParsedRow {
  nome: string;
  turma: string;
  cod_turma: string;
  chamada: number | null;
  termo?: number;
  data_aula?: string;
  disciplina?: string;
  presente?: boolean;
  rowNumber: number;
  errors: string[];
}

export interface ParseResult {
  data: ParsedRow[];
  columnMapping: ColumnMapping;
  warnings: string[];
}

export interface ColumnMapping {
  nome: number | null;
  turma: number | null;
  cod_turma: number | null;
  chamada: number | null;
  termo?: number | null;
  data_aula?: number | null;
  disciplina?: number | null;
  presente?: number | null;
}

export function parseExcelFile(file: File): Promise<ParseResult> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: 'array' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];

        if (!worksheet) {
          reject(new Error('Nenhuma planilha encontrada no arquivo'));
          return;
        }

        // Pega os dados brutos como matriz
        const range = XLSX.utils.decode_range(worksheet['!ref'] || 'A1');
        const rows: unknown[][] = [];

        for (let R = range.s.r; R <= range.e.r; ++R) {
          const row: unknown[] = [];
          for (let C = range.s.c; C <= range.e.c; ++C) {
            const cellAddress = XLSX.utils.encode_cell({ r: R, c: C });
            const cell = worksheet[cellAddress];
            row.push(cell?.v ?? '');
          }
          rows.push(row);
        }

        if (rows.length < 2) {
          reject(new Error('Arquivo deve conter cabeçalho e pelo menos uma linha de dados'));
          return;
        }

        // Primeira linha = headers
        const headersOriginais = (rows[0] as unknown[]).map((h) => String(h || '').trim());

        console.log('Headers originais:', headersOriginais);

        const columnMapping = detectColumns(headersOriginais);

        console.log('Column mapping:', columnMapping);

        if (columnMapping.nome === null || columnMapping.cod_turma === null) {
          reject(
            new Error(
              `Colunas não detectadas. Nome: ${columnMapping.nome}, Cod Turma: ${columnMapping.cod_turma}`
            )
          );
          return;
        }

        const parsedData: ParsedRow[] = [];

        for (let i = 1; i < rows.length; i++) {
          const row = (rows[i] as unknown[]).map((cell) => {
            if (cell === null || cell === undefined) return '';
            return String(cell).trim();
          });

          if (row.every((cell) => cell === '')) continue;

          const parsed = parseRow(row, columnMapping, i + 1);
          parsedData.push(parsed);
        }

        resolve({
          data: parsedData,
          columnMapping,
          warnings: []
        });
      } catch (error) {
        console.error('Erro no parser:', error);
        reject(error);
      }
    };

    reader.onerror = () => reject(new Error('Erro ao ler o arquivo'));
    reader.readAsArrayBuffer(file);
  });
}

function normalizeString(str: string): string {
  return str
    .toLowerCase()
    .trim()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove acentos
    .replace(/[.\-_\s]+/g, ' ') // Normaliza espaços, pontos, traços, underscores
    .trim();
}

function detectColumns(headers: string[]): ColumnMapping {
  const mapping: ColumnMapping = {
    nome: null,
    turma: null,
    cod_turma: null,
    chamada: null,
    termo: null,
    data_aula: null,
    disciplina: null,
    presente: null
  };

  headers.forEach((header, index) => {
    const normalized = normalizeString(header);
    console.log(`Header[${index}]: "${header}" → normalized: "${normalized}"`);

    // Procura por "nome"
    if (normalized === 'nome' || normalized.includes('nome')) {
      if (mapping.nome === null) mapping.nome = index;
    }

    // Procura por "turma"
    if (normalized === 'turma' || normalized.includes('turma')) {
      if (mapping.turma === null && !normalized.includes('cod')) {
        mapping.turma = index;
      }
    }

    // Procura por "cod turma" ou "codigo turma"
    if (normalized.includes('cod') && normalized.includes('turma')) {
      if (mapping.cod_turma === null) mapping.cod_turma = index;
    }

    // Procura por "chamada" ou "n" (número)
    if (normalized.includes('chamada') || normalized === 'n' || normalized === 'n chamada') {
      if (mapping.chamada === null) mapping.chamada = index;
    }

    // Procura por "termo" ou "semestre"
    if (normalized.includes('termo') || normalized.includes('semestre')) {
      if (mapping.termo === null) mapping.termo = index;
    }

    // Procura por "data" + "aula"
    if (normalized.includes('data') && normalized.includes('aula')) {
      if (mapping.data_aula === null) mapping.data_aula = index;
    }

    // Procura por "disciplina"
    if (normalized.includes('disciplina')) {
      if (mapping.disciplina === null) mapping.disciplina = index;
    }

    // Procura por "presente"
    if (normalized.includes('presente')) {
      if (mapping.presente === null) mapping.presente = index;
    }
  });

  console.log('Final mapping:', mapping);
  return mapping;
}

function parseRow(row: string[], mapping: ColumnMapping, rowNumber: number): ParsedRow {
  const errors: string[] = [];

  const nome = mapping.nome !== null ? row[mapping.nome]?.trim() || '' : '';
  const turma = mapping.turma !== null ? row[mapping.turma]?.trim() || '' : '';
  const cod_turma = mapping.cod_turma !== null ? row[mapping.cod_turma]?.trim() || '' : '';
  const chamadaStr = mapping.chamada !== null ? row[mapping.chamada]?.trim() || '' : '';
  const termoStr =
    mapping.termo !== null && mapping.termo !== undefined ? row[mapping.termo]?.trim() || '' : '';
  const data_aula =
    mapping.data_aula !== null && mapping.data_aula !== undefined
      ? row[mapping.data_aula]?.trim() || ''
      : '';
  const disciplina =
    mapping.disciplina !== null && mapping.disciplina !== undefined
      ? row[mapping.disciplina]?.trim() || ''
      : '';
  const presenteStr =
    mapping.presente !== null && mapping.presente !== undefined
      ? row[mapping.presente]?.trim() || ''
      : '';

  // Validações
  if (!nome) {
    errors.push('Nome está vazio');
  }

  if (!cod_turma) {
    errors.push('Código da turma está vazio');
  }

  let chamada: number | null = null;
  if (chamadaStr) {
    const num = parseInt(chamadaStr);
    if (isNaN(num) || num <= 0) {
      errors.push(`Número de chamada inválido: "${chamadaStr}"`);
    } else {
      chamada = num;
    }
  }

  let termo: number | undefined;
  if (termoStr) {
    const num = parseInt(termoStr);
    if (isNaN(num) || num < 1 || num > 6) {
      errors.push(`Termo inválido: "${termoStr}" (deve ser 1-6)`);
    } else {
      termo = num;
    }
  }

  let presente: boolean | undefined;
  if (presenteStr) {
    presente = presenteStr.toLowerCase() === 'true' || presenteStr.toUpperCase() === 'SIM';
  }

  return {
    nome,
    turma,
    cod_turma,
    chamada,
    termo,
    data_aula: data_aula || undefined,
    disciplina: disciplina || undefined,
    presente,
    rowNumber,
    errors
  };
}

export function validateRow(row: ParsedRow): string[] {
  const errors: string[] = [];

  if (!row.nome?.trim()) {
    errors.push('Nome está vazio');
  }

  if (!row.cod_turma?.trim()) {
    errors.push('Código da turma está vazio');
  }

  if (row.chamada !== null && (row.chamada <= 0 || !Number.isInteger(row.chamada))) {
    errors.push('Número de chamada deve ser um inteiro positivo');
  }

  if (row.termo !== undefined && (row.termo < 1 || row.termo > 6)) {
    errors.push('Termo deve estar entre 1 e 6');
  }

  return errors;
}
