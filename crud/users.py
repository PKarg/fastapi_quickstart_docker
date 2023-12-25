from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.user import (UserCreateSchema, UserFilterSchema, UserCreateSchemaHashed)
from .base import CRUDBase
from models.users import User


class UserCrud(CRUDBase):

    @classmethod
    def get_active_player(cls, db: Session, player_id: int):
        return db.execute(select(User).filter(User.status == 1).filter(User.id == player_id)).scalar_one()

    def get_filtered(self, db: Session, filters: List[dict],
                     validation_schema=UserFilterSchema,
                     limit: int = None, offset: int = None):
        return super().get_filtered(db=db, filters=filters,
                                    validation_schema=validation_schema,
                                    limit=limit, offset=offset)

    def create_player(self, db: Session, player_data: UserCreateSchema,
                      player_identifier: str, hashed_password: str):
        obj_in = UserCreateSchemaHashed(hashed_password=hashed_password,
                                        **player_data.model_dump())

        if not obj_in.model_dump().get("identifier"):
            obj_in.identifier = player_identifier

        return super().create(db=db, obj_in=obj_in)


user_crud = UserCrud(User)
