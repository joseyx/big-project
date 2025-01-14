# Big Project

This project is built using FastAPI and can be run using Docker.

## Best Practices

For best practices on using FastAPI, refer to the [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) repository.

## Prerequisites

- Docker
- Docker Compose

## Running the Project

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/big-project.git
   cd big-project
   ```

2. **Build and run the Docker containers:**

   ```sh
   docker-compose up --build
   ```

3. **Access the application:**

   Open your browser and go to `http://localhost:8000`.

## Stopping the Project

To stop the running containers, press `Ctrl+C` in the terminal where `docker-compose` is running, or run:

```sh
docker-compose down
```

## Additional Information

- The application code is located in the `app` directory.
- The `Dockerfile` and `docker-compose.yml` are used to build and run the Docker containers.
- The application exposes port `8000` by default.

For more details, refer to the documentation of [FastAPI](https://fastapi.tiangolo.com/) and [Docker](https://docs.docker.com/).

## Database Migrations

Use these commands to manage your database schema:

```sh
alembic revision --autogenerate -m "[Migration Name]"
alembic upgrade head
alembic downgrade -1
```

run alembic commands inside docker

```sh
docker-compose exec web alembic revision --autogenerate -m "Describe your changes"
docker-compose exec web alembic upgrade head
```

## Readme en Español

Para leer el readme en español, consulta [readme.es.md](readme.es.md).
