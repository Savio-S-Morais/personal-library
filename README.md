# 📚 Gerenciador de Biblioteca Particular <br> 🚧 Em Construção 🚧

Um projeto pessoal focado no controle, organização e visualização de acervos e bibliotecas particulares de forma simples e intuitiva via web.

---

## 🎯 Objetivos do Projeto

### Gerais

- **Visualização Centralizada:** Permitir o acompanhamento visual claro de todas as obras que integram o acervo pessoal.
- **Organização por Coleções:** Categorizar os livros através de marcadores (tags) que identificam a qual coleção pertencem, sendo elas:
  - Coleção 1
  - Coleção 2
  - Coleção 3
  - Coleção Comunitária
- **Acessibilidade:** Facilitar o acesso e a consulta aos dados de maneira responsiva através da web.

### Específicos

- **Contador de Metas:** Implementar um contador dinâmico para exibir quantos livros faltam para que a soma das coleções atinja a marca de uma biblioteca oficial (meta de 1.000 livros).
- **Controle de Acesso (RBAC):** Estruturar permissões para 3 usuários distintos. Todos poderão visualizar as 4 coleções, mas cada usuário terá permissão de edição apenas sobre a sua respectiva coleção privada e a coleção comunitária, com excessão do usuário Administrador, que poderá editar qualquer uma das coleções.
- **Autenticação e Autorização:** Garantir a segurança e o controle dos acessos por meio de um sistema robusto de login e níveis de permissão.

---

## 🛠️ Tecnologias e Arquitetura

### Stack Tecnológica

- **Frontend:** Inicialmente desenvolvido com HTML5, CSS3 e JavaScript Vanilla (com planos futuros de evolução da interface).
- **Backend:** Flask (Python) para o gerenciamento de rotas, lógica de negócios e segurança.
- **Banco de Dados:**
  - Inicialmente: Google Sheets integrados via API.
  - Evolução: PostgreSQL para o armazenamento persistente e relacional dos dados.
- **APIs Externas:**
  - Integração com a [Open Library Covers API](https://openlibrary.org/dev/docs/api/covers) para renderização automática das capas dos livros via ISBN.
  - Google Sheets API para leitura, atualização e adição de novos dados.

### Padrões e Metodologias de Desenvolvimento

- **MVC (Model-View-Controller):** Divisão de responsabilidades para garantir um código modular e atomizado.
- **TDD (Test-Driven Development):** Desenvolvimento orientado a testes, garantindo a qualidade do código, prevenindo regressões e assegurando que cada funcionalidade atenda aos requisitos antes mesmo de sua implementação.
- **Clean Code:** Aplicação de boas práticas de desenvolvimento para facilitar a leitura, manutenção e escalabilidade do sistema.
- **ORM (Object-Relational Mapping):** Utilização de mapeamento objeto-relacional para simplificar as operações de CRUD no banco de dados.

---

## 📐 Modelagem do Banco de Dados (DER)

> Será utilizado futuramente quando ocorrer a migração Google Sheets para PostgreSQL

O banco de dados é composto por tabelas normalizadas que garantem a integridade referencial do acervo.

### 1. Livro

- `ID_Livro`: INT [PK] [NN]
- `titulo`: VARCHAR(255) [NN]
- `anoPublicacao`: INT [NN]
- `ISBN`: VARCHAR(13) [NN]
- `status`: VARCHAR(50) [NN] _(Valores: Disponível, Em leitura, Emprestado, Desaparecido)_
- `ID_Autor`: INT [FK -> Autor.ID_Autor] [NN]
- `ID_Editora`: INT [FK -> Editora.ID_Editora] [NN]
- `ID_Colecao`: INT [FK -> Colecao.ID_Colecao] [NN]
- **Relacionamentos:** N:1 com Autor, N:1 com Editora, N:1 com Coleção.

### 2. Autor

- `ID_Autor`: INT [PK] [NN]
- `nomeAutor`: VARCHAR(150) [NN]
- **Relacionamento:** 1:N com Livro.

### 3. Coleção

- `ID_Colecao`: INT [PK] [NN]
- `nomeColecao`: VARCHAR(100) [NN]
- **Relacionamento:** 1:N com Livro.

### 4. Editora

- `ID_Editora`: INT [PK] [NN]
- `nomeEditora`: VARCHAR(100) [NN]
- **Relacionamento:** 1:N com Livro.

### 5. Categoria

- `ID_Categoria`: INT [PK] [NN]
- `nomeCategoria`: VARCHAR(50) [NN]
- **Relacionamento:** 1:N com Livro-Categoria.

### 6. Livro-Categoria (Tabela Pivô)

- `ID_Livro`: INT [FK -> Livro.ID_Livro] [NN]
- `ID_Categoria`: INT [FK -> Categoria.ID_Categoria] [NN]
- **Relacionamento:** Resolve a relação N:N entre as tabelas Livro e Categoria.

---

## 🔄 Endpoints e Rotas da Aplicação

### Visualização e Páginas Web

- `/` -> **Home Principal:** Exibe uma visão geral de todos os livros cadastrados em formato de catálogo (estilo _Letterboxd_). No topo, exibe a contagem regressiva _"Faltam XX livros para ser considerado uma biblioteca"_. Ao atingir 1.000 livros, o texto muda para _"Bem-vindo à nossa biblioteca"_.
- `/login` -> Tela de autenticação de usuários.
- `/logout` -> Encerramento da sessão ativa.
- `/sobre` -> Informações sobre o projeto e o desenvolvedor.
- `/<string:nomeColecao>` -> Filtro do catálogo focado exclusivamente na coleção informada na URL.
- `/<string:url>` -> Rota de fallback para tratamento de erros e escapes (Página 404).

### Operações Administrativas

- `/adicionar` -> Formulário para o cadastro de novos livros.
- `/atualizar` -> Tela para edição e atualização de dados dos livros existentes.
- `/adminPanel` -> Painel de controle exclusivo para o usuário administrador.

### API (Roadmap Futuro)

- `/api/v1` -> Endpoint planejado para disponibilizar os dados da biblioteca em formato JSON para integração com outros projetos.
- `/api/v1/status` -> Retorna o status atual da conexão e da API.
