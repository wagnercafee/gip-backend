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
pip install -r requirements.txt

echo "Ambiente pronto!"
