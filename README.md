# Floreios e Borrões — Catálogo Digital

Plataforma web de catálogo digital para a livraria Floreios e Borrões, permitindo que clientes consultem o acervo e a disponibilidade de títulos remotamente, e que administradores gerenciem o inventário.

## Equipe

| Nome | Papel |
|---|---|
| Anderson Rodrigues | - |
| Brunno Colombo | - |
| João Vitor Santos | - |

---

## Stack

| Camada | Tecnologia |
|---|---|
| Back-end | Python 3.13+ (FastAPI) |
| Front-end | React 19+ *ou* HTML + CSS + JS (a definir) |
| Banco de Dados | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| Storage | Supabase Storage (capas dos livros) |

---

## Funcionalidades

### Cliente
- Busca por título, autor ou gênero
- Catálogo com capa, sinopse e preço
- Status de estoque em tempo real
- Filtros por categoria (Ficção, Não-ficção, Clássicos)

### Administrador
- CRUD completo do catálogo
- Upload de metadados (ISBN, editora, ano) e imagem de capa
- Controle de quantidade em estoque
- Painel de visão geral do acervo

---

## Estrutura do Projeto

```
floreios-e-borroes/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── (React ou HTML/CSS/JS)
└── README.md
```

---

## Configuração do Ambiente

### Pré-requisitos

- Python 3.13+
- Node.js 22+ *(se front-end em React)*
- Conta no [Supabase](https://supabase.com)

### Back-end

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Preencha o `.env`:

```env
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_KEY=<service_role_key>
```

```bash
uvicorn app.main:app --reload
```

API disponível em `http://localhost:8000`. Documentação automática em `/docs`.

### Front-end (React)

```bash
cd frontend
npm install
npm run dev
```

---

## Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `SUPABASE_URL` | URL do projeto Supabase |
| `SUPABASE_KEY` | Chave de serviço do Supabase |

---

## Banco de Dados

O schema é gerenciado via Supabase. As migrations ficam em `backend/migrations/` *(a definir)*.

Tabelas principais:

- `books` — acervo com metadados e quantidade em estoque
- `categories` — categorias/gêneros literários

---

## Decisões em Aberto

- [ ] Definir framework do front-end (React vs HTML+CSS+JS)
- [ ] Definir estratégia de autenticação do administrador (Supabase Auth vs JWT próprio)
- [ ] Definir hospedagem (Vercel, Render, Railway, etc.)
