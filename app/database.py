import importlib
import logging
import os
import pkgutil
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@postgres:5432/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def discover_models():
    package_dir = os.path.dirname(__file__)
    for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
        if is_pkg:
            schemas_path = os.path.join(package_dir, module_name, 'schemas.py')
            if os.path.exists(schemas_path):
                try:
                    importlib.import_module(f"app.{module_name}.schemas")
                    logger.info(f"Successfully imported app.{module_name}.schemas")
                except ImportError as e:
                    logger.error(f"Error importing app.{module_name}.schemas: {e}")
            else:
                logger.info(f"No schemas.py in app.{module_name}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]