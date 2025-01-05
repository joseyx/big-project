import logging
from fastapi import FastAPI

from app.config.utils import discover_routers
from app.auth.router import router

logger = logging.getLogger(__name__)

app = FastAPI()

# Auto-discover and include all routers
logger.info("Discovering routers...")
routers = discover_routers()
for router in routers:
    app.include_router(router)