import logging
import os

import uvicorn

from config import project_settings

if __name__ == "__main__":
    os.environ["ENVIRONMENT"] = "dev"

    uvicorn.run("main:app",
                log_level=logging.INFO,
                host=project_settings.main_settings.uvicorn_host,
                port=project_settings.main_settings.uvicorn_port,
                reload=True,
                reload_dirs=["routers", "models",
                             "utils", "db", "crud", "main.py"])
