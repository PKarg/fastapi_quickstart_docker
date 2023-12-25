import datetime
import hashlib
import secrets
from typing import Optional, List

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError
from typing_extensions import Annotated

from crud.users import user_crud
from db.setup import get_db
from models.users import User
from run.config import project_settings

security = HTTPBasic()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth/token")


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def create_user_identifier() -> str:
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:12]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def check_docs_access(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username,
                                              project_settings.main_settings.docs_username)
    correct_password = secrets.compare_digest(credentials.password,
                                              project_settings.main_settings.docs_password)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credentials.username


def create_access_token(username: str, user_id: int, expire_days: Optional[int] = None):
    data_to_encode = {"sub": username, "id": user_id}
    if expire_days:
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=expire_days)
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            days=project_settings.main_settings.auth_token_expire_days)
    data_to_encode.update({"exp": expire})
    return jwt.encode(data_to_encode, project_settings.main_settings.auth_secret_key.get_secret_value(),
                      algorithm=project_settings.main_settings.auth_algorithm)


def authenticate_user(username: str, password: str, db: Session) -> User | bool:
    u: List[User] = user_crud.get_filtered_by(db=db, name=username)
    user: User = u[0] if u else None
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


class TokenData(BaseModel):
    id: int
    username: str | None = None


def get_current_active_user(token: Annotated[str, Depends(oauth2_scheme)],
                            db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, project_settings.main_settings.auth_secret_key,
                             project_settings.main_settings.auth_algorithm)
        username: str = payload.get("sub")
        id: int = payload.get("id")
        if not username or not id:
            raise credentials_exception
        token_data = TokenData(id=id, username=username)
    except JWTError:
        raise credentials_exception
    user = user_crud.get_active_user(db=db, user_id=token_data.id)
    if not user:
        raise credentials_exception
    return user
