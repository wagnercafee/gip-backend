#!/bin/bash

# Cria o venv se não existir
if [ ! -d ".venv" ]; then
  echo "Criando ambiente virtual (.venv)..."
  python3 -m venv .venv
fi

# Ativa o venv
source .venv/bin/activate

# Instala as dependências
echo "Instalando dependências..."
pip install -r requirements-dev.txt

echo "Ambiente pronto!"

uvicorn src.main:app --host 0.0.0.0 --port 9090 --reload
