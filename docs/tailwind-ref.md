# 🎨 Classes Tailwind CSS — Referência Rápida

---

## Layout e Posicionamento

```
flex             → display: flex
items-center     → alinha verticalmente no centro (eixo Y)
justify-center   → alinha horizontalmente no centro (eixo X)
justify-between  → espaça os filhos nas extremidades
gap-4            → espaço de 1rem entre filhos do flex
flex-col         → direção do flex em coluna
flex-wrap        → permite quebrar linha

grid             → display: grid
grid-cols-3      → 3 colunas iguais
col-span-2       → ocupa 2 colunas
```

---

## Tamanho e Espaçamento

> 1 unidade = 0.25rem (4px)

```
p-4      → padding 1rem em todos os lados
px-4     → padding 1rem esquerda e direita
py-2     → padding 0.5rem cima e baixo
pt-6     → padding-top 1.5rem

m-4      → margin 1rem
mx-auto  → centraliza horizontalmente (margin: 0 auto)
mt-8     → margin-top 2rem
mb-4     → margin-bottom 1rem

w-full      → width: 100%
w-64        → width: 16rem (256px)
max-w-md    → largura máxima 28rem — bom para cards
max-w-xl    → largura máxima 36rem
min-h-screen → altura mínima de 100vh
h-10        → height: 2.5rem
```

---

## Tipografia

```
text-sm       → 0.875rem
text-base     → 1rem (padrão)
text-lg       → 1.125rem
text-xl       → 1.25rem
text-2xl      → 1.5rem
text-3xl      → 1.875rem

font-normal   → peso 400
font-medium   → peso 500
font-semibold → peso 600
font-bold     → peso 700

text-center   → alinha ao centro
text-left     → alinha à esquerda

text-gray-500  → cinza médio (subtítulos)
text-gray-800  → cinza escuro (títulos)
text-white     → branco
text-red-600   → vermelho (erros)
text-green-600 → verde (sucesso)
text-blue-600  → azul (links, destaques)

uppercase       → TEXTO EM MAIÚSCULO
tracking-wide   → espaçamento entre letras
leading-relaxed → espaçamento entre linhas largo
truncate        → corta texto com "..."
```

---

## Cores de Fundo

```
bg-white      → branco
bg-gray-50    → cinza quase branco (fundo de página)
bg-gray-100   → cinza claro
bg-gray-800   → cinza escuro
bg-blue-600   → azul (botão primário)
bg-red-600    → vermelho (SENAI, erros, deletar)
bg-green-50   → verde bem claro (linha presente)
bg-red-50     → vermelho bem claro (linha ausente)
```

---

## Bordas e Sombras

```
border          → borda 1px solid
border-2        → borda 2px
border-gray-200 → cor da borda cinza claro
border-red-500  → borda vermelha

rounded         → border-radius 0.25rem
rounded-lg      → border-radius 0.5rem
rounded-xl      → border-radius 0.75rem
rounded-2xl     → border-radius 1rem
rounded-full    → círculo perfeito

shadow          → sombra sutil
shadow-md       → sombra média
shadow-lg       → sombra pronunciada
shadow-none     → remove sombra
```

---

## Estados Interativos

```
hover:bg-blue-700        → muda fundo no hover
hover:text-white         → muda cor do texto no hover
hover:shadow-lg          → adiciona sombra no hover

focus:outline-none       → remove outline padrão do browser
focus:ring-2             → adiciona anel de foco
focus:ring-blue-500      → cor do anel de foco

active:scale-95          → encolhe levemente ao clicar

disabled:opacity-50      → opacidade 50% quando desativado
disabled:cursor-not-allowed → cursor de proibido quando desativado
```

---

## Transições

```
transition         → transição em todas as propriedades
transition-colors  → só transiciona cores (mais performático)
transition-shadow  → só transiciona sombra
duration-200       → 200ms
duration-300       → 300ms
ease-in-out        → curva de animação suave
```

---

## Exemplos do Projeto

**Linha da tabela de presença**
```svelte
<tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
```

**Botão presente / ausente**
```svelte
<button class="bg-green-100 text-green-700 text-sm font-medium px-3 py-1 rounded-full">
  ✅ Presente
</button>

<button class="bg-red-100 text-red-700 text-sm font-medium px-3 py-1 rounded-full">
  ❌ Ausente
</button>
```

**Card de turma**
```svelte
<div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
```

**Input de formulário**
```svelte
<input class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
              focus:outline-none focus:ring-2 focus:ring-blue-500">
```

**Badge de porcentagem**
```svelte
<span class="bg-blue-100 text-blue-700 text-xs font-semibold px-2 py-1 rounded-full">
  87%
</span>
```


```