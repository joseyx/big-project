import importlib
import os
import pkgutil
from typing import List, Tuple
import logging

import bcrypt
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

def discover_routers() -> List[Tuple]:
    routers = []
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Apunta a 'app/'

    # Utilizar pkgutil.walk_packages con el prefijo adecuado
    for finder, module_name, is_pkg in pkgutil.walk_packages([app_dir], prefix='app.'):
        if is_pkg:
            try:
                # Intentar importar 'app.{module_name}.router'
                full_module_name = f"{module_name}.router"
                module = importlib.import_module(full_module_name)

                # Verificar si el módulo tiene un atributo 'router'
                if hasattr(module, 'router'):
                    router = module.router

                    # Extraer el prefijo basado en el nombre del módulo
                    # Eliminar el prefijo 'app' para evitar '/app/auth'
                    path_parts = module_name.split('.')
                    if path_parts[0] == 'app':
                        path_parts = path_parts[1:]  # Eliminar 'app'

                    prefix = '/' + '/'.join(path_parts) if path_parts else '/'

                    routers.append((router, prefix))
                    logger.info(f"Successfully imported {full_module_name} with prefix '{prefix}'")
            except (ImportError, AttributeError) as e:
                logger.error(f"Error importing {full_module_name}: {e}")
    return routers

async def custom_exception_handler(request: Request, exc: Exception):
    # Retrieve the Request ID from headers or generate a new one
    request_id = request.headers.get("X-Request-ID", "unknown")
    
    # Log the exception with the Request ID
    logger.warning(f"Request ID: {request_id} - Exception: {exc}")
    
    # Return a JSON response with the Request ID
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "request_id": request_id},
    )

# Hash a password using bcrypt
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8') 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')  # Convertir str a bytes
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)