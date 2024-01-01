from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from run.config import project_settings
from db.setup import get_db
from auth.functions import create_access_token, check_docs_access, authenticate_user, \
    get_password_hash
from crud.users import user_crud, create_user_identifier
from schemas.users import UserCreateSchema

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

security = HTTPBasic()


@user_router.post("/auth/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(username=user.username, user_id=user.user_id,
                                       expire_days=project_settings.token_expire_days)
    return {"access_token": access_token}


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_user(user_data: UserCreateSchema, db: Session = Depends(get_db),
                          username: str = Depends(check_docs_access)):
    user = user_crud.get_filtered_by(db=db, name=user_data.name)
    if user:
        raise HTTPException(status_code=400, detail="Player already exists")
    else:
        user_id = create_user_identifier()
        hashed_password = get_password_hash(user_data.raw_password)
        user = user_crud.create_user(db=db, user_data=user_data,
                                     user_identifier=user_id, hashed_password=hashed_password)
    return user
