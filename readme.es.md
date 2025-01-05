# Gran Proyecto

Este proyecto está construido usando FastAPI y se puede ejecutar usando Docker.

## Mejores practicas

Para las mejores practicas de FastAPI, revisa el repositorio [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices).

## Requisitos Previos

- Docker
- Docker Compose

## Ejecutando el Proyecto

1. **Clona el repositorio:**

   ```sh
   git clone https://github.com/yourusername/big-project.git
   cd big-project
   ```

2. **Construye y ejecuta los contenedores Docker:**

   ```sh
   docker-compose up --build
   ```

3. **Accede a la aplicación:**

   Abre tu navegador y ve a `http://localhost:8000`.

## Deteniendo el Proyecto

Para detener los contenedores en ejecución, presiona `Ctrl+C` en la terminal donde se está ejecutando `docker-compose`, o ejecuta:

```sh
docker-compose down
```

## Información Adicional

- El código de la aplicación se encuentra en el directorio `app`.
- El `Dockerfile` y `docker-compose.yml` se utilizan para construir y ejecutar los contenedores Docker.
- La aplicación expone el puerto `8000` por defecto.

Para más detalles, consulta la documentación de [FastAPI](https://fastapi.tiangolo.com/) y [Docker](https://docs.docker.com/).

## Migraciones de la Base de Datos

Usa estos comandos para administrar el esquema de tu base de datos:

```sh
alembic revision --autogenerate -m "[Nombre de la migración]"
alembic upgrade head
alembic downgrade -1
```
