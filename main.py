from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from auth.functions import check_docs_access
from db.setup import Base, engine
from routers.users import user_router
from models.users import User

Base.metadata.create_all(engine)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(user_router)


@app.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(check_docs_access)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(check_docs_access)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)
