Rodar projeto localmente

$ docker compose up -d --build

Aqui ira subir o backend que pode ser acessado via localhost:9090

Sobe o banco de dados tambem um postgres que pode ser acessado via dbeaver localhost:9091
Utilizar o environment do arquivo docker-compose.yml para configurar o dbeaver.

Para instalar Bibliotecas deve se coloca-las no requirements.txt e rodar novamente:

Se o docker estiver rodando é bom derruba-lo com :
$ docker compose down

e depois:
$ docker compose up -d --build