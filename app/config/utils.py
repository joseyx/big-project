import importlib
import os
import pkgutil
from typing import List
import logging

logger = logging.getLogger(__name__)

def discover_routers() -> List:
    routers = []
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Points to 'app/'
    for finder, module_name, is_pkg in pkgutil.walk_packages([app_dir]):
        if is_pkg:
            try:
                # Attempt to import 'app.{module_name}.router'
                module = importlib.import_module(f"app.{module_name}.router")
                routers.append(module.router)
                logger.info(f"Successfully imported app.{module_name}.router")
            except (ImportError, AttributeError) as e:
                logger.error(f"Error importing app.{module_name}.router: {e}")
    return routers