# Requisitos

## Definição do Problema

A livraria física possui um acervo vasto e rotativo, dificultando que clientes saibam se um título está disponível antes de se deslocarem até o local. A ausência de catálogo digital impede que novos leitores conheçam a curadoria remotamente, limitando o alcance ao público que transita fisicamente pela região.

---

## Ambiente de Execução

- **Plataforma:** Navegadores web (desktop e mobile)
- **Contexto:** Extensão digital de uma livraria física localizada em centro histórico
- **Proposta:** Simular a organização de uma biblioteca física com estantes digitais, priorizando calmaria e imersão literária

---

## Perfis de Usuário

| Perfil | Descrição |
|---|---|
| Cliente | Leitores, estudantes e pesquisadores (18–65 anos) que buscam curadoria de títulos e praticidade na consulta |
| Administrador | Funcionários da livraria responsáveis pela gestão do acervo, com perfil técnico básico |

---

## Requisitos Funcionais

### Cliente

- Barra de busca por título, autor ou gênero
- Catálogo digital com capa, sinopse e preço
- Status de estoque em tempo real
- Filtros por categoria (Ficção, Não-ficção, Clássicos)

### Administrador

- CRUD completo do catálogo
- Upload de metadados (ISBN, editora, ano de publicação) e imagem de capa
- Controle de quantidade em estoque por título
- Painel de visão geral de todos os itens cadastrados