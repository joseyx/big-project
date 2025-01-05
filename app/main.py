import logging
from fastapi import FastAPI

from app.config.middleware import add_middlewares
from app.config.utils import discover_routers
from app.auth.router import router

logger = logging.getLogger(__name__)

app = FastAPI()

# Add middleware to the app
add_middlewares(app)

# Auto-discover and include all routers
logger.info("Discovering routers...")
routers = discover_routers()
for router, prefix in routers:
    app.include_router(router, prefix=prefix)
    logger.info(f"Incluido router con prefijo '{prefix}'")
