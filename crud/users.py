import hashlib
import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.users import (UserCreateSchema, UserFilterSchema, UserCreateSchemaHashed)
from crud.base import CRUDBase
from models.users import User


def create_user_identifier() -> str:
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:12]


class UserCrud(CRUDBase):

    @classmethod
    def get_active_user(cls, db: Session, user_id: int):
        return db.execute(select(User).filter(User.status == 1).filter(User.id == user_id)).scalar_one()

    def get_filtered(self, db: Session, filters: List[dict],
                     validation_schema=UserFilterSchema,
                     limit: int = None, offset: int = None):
        return super().get_filtered(db=db, filters=filters,
                                    validation_schema=validation_schema,
                                    limit=limit, offset=offset)

    def create_user(self, db: Session, user_data: UserCreateSchema, hashed_password: str):
        user_identifier = create_user_identifier()
        obj_in = UserCreateSchemaHashed(hashed_password=hashed_password,
                                        **user_data.model_dump())

        if not obj_in.model_dump().get("identifier"):
            obj_in.identifier = user_identifier

        return super().create(db=db, obj_in=obj_in)


user_crud = UserCrud(User)
