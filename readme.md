# Big Project

This project is built using FastAPI and can be run using Docker.

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

## Readme en Español

Para leer el readme en español, consulta [readme.es.md](readme.es.md).
