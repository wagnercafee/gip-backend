# Dockerfile
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos para o container
COPY . /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expôr a porta 9090 no container
EXPOSE 9090

# Rodar o servidor FastAPI na porta 9090
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090", "--reload"]
