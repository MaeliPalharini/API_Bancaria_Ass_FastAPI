# 💰API Bancária Assíncrona com FastAPI

Neste projeto, desenvolvemos uma API RESTful assíncrona utilizando FastAPI para gerenciar operações bancárias de depósitos e saques, vinculadas a contas correntes. Este projeto proporciona a experiência de construir uma aplicação backend moderna e eficiente que utiliza autenticação JWT e práticas recomendadas de design de APIs.

**Nota:** Este projeto foi desenvolvido com fins educacionais, para demonstrar o uso de FastAPI em aplicações bancárias e a implementação de autenticação JWT.

## 💫Objetivos e Funcionalidades

O objetivo deste projeto é desenvolver uma API com as seguintes funcionalidades:

- **Cadastro de Transações**: Permite o cadastro de transações bancárias, como depósitos e saques.
- **Exibição de Extrato**: Implementa um endpoint para exibir o extrato de uma conta, mostrando todas as transações realizadas.
- **Autenticação com JWT**: Utiliza JWT (JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar os endpoints que exigem autenticação.

## 👷Requisitos Técnicos

Para a realização deste projeto, foram atendidos os seguintes requisitos técnicos:

- **FastAPI**: Utiliza FastAPI como framework para criar a API. Aproveita os recursos assíncronos do framework para lidar com operações de I/O de forma eficiente.
- **Modelagem de Dados**: Cria modelos de dados adequados para representar contas correntes e transações. Garante que as transações estão relacionadas a uma conta corrente, e que contas possam ter múltiplas transações.
- **Validação das Operações**: Não permite depósitos e saques com valores negativos, valida se o usuário possui saldo para realizar o saque.
- **Segurança**: Implementa autenticação usando JWT para proteger os endpoints que necessitam de acesso autenticado.
- **Documentação com OpenAPI**: Certifica-se de que a API esteja bem documentada, incluindo descrições adequadas para cada endpoint, parâmetros e modelos de dados.

## 🔧🔨Tecnologias Usadas

- **FastAPI**: Framework web moderno e rápido para construir APIs com Python 3.6+ baseado em padrões OpenAPI e JSON Schema.
- **SQLite**: Banco de dados SQL leve e autônomo.
- **SQLAlchemy**: ORM (Object Relational Mapper) para interagir com o banco de dados.
- **Alembic**: Ferramenta de migração de banco de dados para SQLAlchemy.
- **Pydantic**: Para validação de dados usando tipagem do Python.
- **JWT (JSON Web Tokens)**: Para autenticação segura.
- **Uvicorn**: Servidor ASGI rápido, usado para servir a aplicação FastAPI.
- **pytest**: Framework de testes para garantir a qualidade do código.
- **Insomnia** Para testes de API.

## 🏗️Configuração do Ambiente

### Requisitos

- Python 3.8+
- Virtualenv ou Conda para gerenciamento de ambientes virtuais

### Passos para Configuração

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/seu-usuario/api_bancaria.git
    cd api_bancaria
    ```

2. **Crie um ambiente virtual**:

    Com Virtualenv:
    ```bash
    python -m venv api_bancaria_env
    source api_bancaria_env/bin/activate  # No Windows use `api_bancaria_env\Scripts\activate`
    ```

    Com Conda:
    ```bash
    conda create -n api_bancaria_env python=3.11
    conda activate api_bancaria_env
    ```

3. **Instale as dependências**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Inicialize o banco de dados**:

    Execute o seguinte comando para criar as tabelas no banco de dados:

    ```python
    from app.database import engine, Base
    from app import models

    Base.metadata.create_all(bind=engine)
    ```

5. **Execute a aplicação**:

    ```bash
    uvicorn app.main:app --reload
    ```

6. **Acesse a documentação da API**:

    A documentação automática da API estará disponível em:
    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## ✨Endpoints Principais

### Autenticação

- `POST /token`: Autentica o usuário e retorna um token JWT.

### Clientes

- `POST /clientes/`: Cria um novo cliente.
- `GET /clientes/{cpf}`: Retorna as informações de um cliente baseado no CPF.

### Contas

- `GET /contas/{cpf}`: Retorna as contas associadas a um cliente.

### Transações

- `POST /depositar/`: Realiza um depósito em uma conta.
- `POST /sacar/`: Realiza um saque de uma conta.
- `GET /extrato/{cpf}`: Retorna o extrato de transações de uma conta.

### Testes
Para executar os testes, utilize o comando:

```bash
pytest
```
## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE]para mais detalhes.

MIT License

Copyright (c) 2024 [Maeli Palharini]

## ✍️ Autora

- [Maeli Palharini](https://github.com/maelipalharini)
