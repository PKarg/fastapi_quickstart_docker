from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from email_validator import validate_email, EmailNotValidError

from db.setup import Base

from models.annotations import int_pk
from models.model_utils import TimestampMixin, TableNameMixin
from models.common_validators import common_string_validator


class User(Base, TableNameMixin, TimestampMixin):
    user_id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(String(length=255), nullable=True)
    email_address: Mapped[str] = mapped_column(String(length=255), nullable=False)
    language_code: Mapped[str] = mapped_column(String(length=8), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    status: Mapped[int] = mapped_column(default=1, nullable=False)  # 0 - inactive, 1 - active, 2 - banned
    auth_level: Mapped[int] = mapped_column(default=0, nullable=False)  # 0 - player, 1 - admin, 2 - superadmin
    identifier: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)

    __table_args__ = (
        CheckConstraint("length(name) > 5", name="name_at_least_5_chars"),
        CheckConstraint("status in (0, 1, 2)", name="status_in_range"),
        CheckConstraint("auth_level in (0, 1, 2)", name="auth_level_in_range"),
    )

    @validates("email")
    def validate_email(self, key: str, address: str):
        try:
            validate_email(address)
        except EmailNotValidError as e:
            raise ValueError("Email address is not valid") from e
        return address

    @validates("name")
    def validate_name(self, key: str, name: str):
        return common_string_validator(name, 5, 30, True)

    @validates("status", "auth_level")
    def validate_statuses(self, key: str, value: int):
        if not isinstance(value, int):
            raise ValueError("Status has to be an integer")
        if value not in (0, 1, 2):
            raise ValueError("Status has to be 0, 1 or 2")
        return value
