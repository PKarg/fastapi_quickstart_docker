import logging
import os

import uvicorn

from config import project_settings

if __name__ == "__main__":
    os.environ["ENVIRONMENT"] = "dev"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    uvicorn.run("main:app",
                log_level=logging.INFO,
                host=project_settings.main.uvicorn_host,
                port=project_settings.main.uvicorn_port,
                reload=True,
                reload_dirs=[f"{project_root}/routers", f"{project_root}/models",
                             f"{project_root}/utils", f"{project_root}/db", f"{project_root}/crud"])
