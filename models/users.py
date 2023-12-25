from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.setup import Base

from annotations import int_pk
from model_utils import TimestampMixin, TableNameMixin


class User(Base, TableNameMixin, TimestampMixin):
    user_id: int_pk
    username: Mapped[str] = mapped_column(String(length=255), nullable=True)
    email_address: Mapped[str] = mapped_column(String(length=255), nullable=False)
    language_code: Mapped[str] = mapped_column(String(length=8), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=255), nullable=False)
