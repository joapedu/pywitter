# Pywitter

<p float="left">
 <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
 <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
 <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white">
 <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white">
</p>

## Instruções Docker: 🐳
Para executar o projeto em **modo de desenvolvimento** com Docker e visualizar a operação, siga os passos abaixo.

### Pré-requisitos:
Ferramentas necessárias para rodar o projeto:
- **Docker** 🐳<br>
   [Guia de Instalação do Docker](https://docs.docker.com/get-docker/).
- **Docker Compose** 🐳<br>
   [Guia de Instalação do Docker Compose](https://docs.docker.com/compose/install/).
  
### Executando o Projeto com Docker:
- Primeiro configure as variáveis de ambiente a partir do arquivo [*.env-exemplo*](./.env-exemplo)

- Após isso, os comandos abaixo realizam a compilação e execução do projeto:

```sh
docker-compose up --build
```

Esse comando irá compilar a imagem Docker e subir os contêineres para o Django e PostgreSQL, com base nas configurações definidas no [docker-compose.yml](./docker-compose.yml).

> O orquestrador possui apenas dois services (backend e db).

> Para visualizar as rotas do backend, acesse localhost:8000/api/

### Executando o Projeto Local:
- Backend:
    - na pasta _backend/_ rode os comandos:
    ```sh
    python -m venv venv
    venv/scripts/activate
    pip install -r ../requirements.txt
    python manage.py runserver
    ```
> Para visualizar as rotas do backend, acesse localhost:8000/api/


### Swagger
- Para uma melhor visualização da estrutura de APIs foi feito com Swagger.

*Por joão Eduardo Braga.*