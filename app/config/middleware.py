import os
import time
import uuid
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
import logging

from app.config.utils import custom_exception_handler

logger = logging.getLogger(__name__)

# Custom Logging Middleware
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Obtener el Request ID de los encabezados o generar uno nuevo
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        # Obtener los últimos 6 caracteres del Request ID
        short_request_id = request_id[-6:]
        # Registrar información de la solicitud con el Request ID acortado
        logger.info(f"Request ID: {short_request_id} - {request.method} {request.url}")
        # Procesar la solicitud
        response = await call_next(request)
        # Registrar información de la respuesta con el Request ID acortado
        logger.info(f"Request ID: {short_request_id} - Response status: {response.status_code}")
        return response
    
# Custom Request ID Middleware
class CustomRequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    
# Custom Exception Handling Middleware
class CustomExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            return await custom_exception_handler(request, exc)
        
# Custom Performance Monitoring Middleware
class CustomPerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        response.headers["X-Response-Time"] = str(end_time - start_time)
        return response

def add_middlewares(app):

    # Request ID Middleware
    app.add_middleware(CustomRequestIDMiddleware)

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # GZip Middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Session Middleware
    secret_key = os.getenv("SECRET_KEY", "default-secret-key")  # Ensure to set a strong secret key in production
    app.add_middleware(SessionMiddleware, secret_key=secret_key)
    
    # Exception Handling Middleware
    app.add_middleware(CustomExceptionMiddleware)

    # Performance Monitoring Middleware
    app.add_middleware(CustomPerformanceMiddleware)
    
    # Logging Middleware
    # app.add_middleware(LogMiddleware)
