#!/bin/bash

# Verifica se o venv está disponível
python3 -m venv --help > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "❌ O módulo 'venv' não está instalado."
  echo "Para instalar no Ubuntu/Debian, execute:"
  echo "  sudo apt install python3-venv"
  exit 1
fi

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

# Verifica se o arquivo .env.local existe
if [ -f ".env.dev" ]; then
  export $(cat .env.dev | xargs)
else
  echo "Arquivo .env.dev não encontrado! Certifique-se de que ele existe."
  exit 1
fi

echo "Ambiente pronto!"

uvicorn src.main:app --host 0.0.0.0 --port 9090 --reload
