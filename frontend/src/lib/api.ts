const BASE = 'http://localhost:8000';

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