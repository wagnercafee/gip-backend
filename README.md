# 🚀 GIP Backend

Backend do projeto **GIP** utilizando **FastAPI** e **PostgreSQL**, com ambiente isolado via **Docker**. Também é possível rodar localmente com Python para desenvolvimento.

---
## 🛠️ Tecnologias
- 🐍 Python 3.9  
- ⚡ FastAPI  
- 🐘 PostgreSQL 15  
- 🐳 Docker + Docker Compose  
---

## ▶️ Como rodar o projeto com Docker

### 1. Pré-requisitos
Certifique-se de ter o **Docker** e o **Docker Compose** instalados.

### 2. Subir o ambiente
```bash
docker compose up -d --build
```
Acesse a API: http://localhost:9090

### 3. Acesso ao banco de dados
Use PgAdmin4, DBeaver ou outro cliente PostgreSQL com os dados abaixo:

#### Environment:

```bash
Host: localhost  
Porta: 9091  
Usuário: gipuser  
Senha: gippass  
Banco de Dados: gipdb  
```

### 4. Como rodar localmente (sem Docker)
Pre-Requisitos 

- Python 3.9 instalado na máquina

#### Execute o script de setup:
```bash
./setupLocal.sh
```

Esse comando irá:

- Criar o ambiente virtual .venv (caso não exista)
- Ativar o ambiente virtual
- Instalar as dependências do requirements-dev.txt

### 5. Rodar a API localmente:

 #### Após o ambiente estar pronto, execute:

```bash
uvicorn main:app --host 0.0.0.0 --port 9090 --reload
```

A API estará disponível em: http://localhost:9090

### 6. Como instalar novas bibliotecas Python
➤ Se estiver usando Docker(**recomendado**):
- Adicione a biblioteca desejada no arquivo requirements.txt

#### Rebuild o container:
```bash
docker compose down
docker compose up -d --build
```

➤ Se estiver rodando localmente:
#### Ative o ambiente virtual:
```bash
source .venv/bin/activate
```

#### Instale a nova biblioteca:
```bash
pip install <nome-da-biblioteca>
```

#### Atualize o requirements-dev.txt:
```bash
pip freeze > requirements-dev.txt
```
ℹ️ Sobre o arquivo requirements-dev.txt
Este arquivo é usado apenas para desenvolvimento local. Ele inclui:

- Todas as libs essenciais (-r requirements.txt)

- Bibliotecas extras úteis para desenvolvimento (ex: linters, debuggers, etc.)

- Sempre que instalar uma nova lib no ambiente local, atualize com:

```bash
pip freeze > requirements-dev.txt
```

**requirements.txt só deve possuir as bibliotecas realmente nescessarias!**
