from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Sequence, Iterable

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, Row, RowMapping, ScalarResult, inspect, Select, delete
from sqlalchemy.orm import Session

from db.setup import Base
from utils.filtering import apply_filters_to_query, BaseFilterSchema

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete.
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.scalars(select(self.model).filter(self.model.id == id)).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Sequence[Row | RowMapping | Any]:
        return db.scalars(select(self.model).offset(skip).limit(limit)).all()

    def get_filtered_by(self, db: Session, **kwargs) -> Sequence[Row | RowMapping | Any]:
        return db.execute(select(self.model).filter_by(**kwargs)).scalars().all()

    def get_filtered(self, db: Session, filters: List[dict],
                     validation_schema: BaseFilterSchema,
                     limit: Optional[int] = 100,
                     offset: Optional[int] = 0) -> Sequence[Row | RowMapping | Any]:
        """
        Apply filter cascade

        :param validation_schema: pydantic schema for filter validation
        :param db: orm session object
        :param filters: iterable of filters, i.e (ModelType.val1 > 10, ModelType.val2 < 3) etc
        :param limit: limit number of returned objects up to value
        :param offset: offset
        :return: list of ModelType
        """
        q = select(self.model)
        q = apply_filters_to_query(query=q, model=self.model,
                                   filters=filters, validation_schema=validation_schema)
        q = q.limit(limit).offset(offset)
        result = db.scalars(q).all()
        return result

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            db_obj = self.model(**obj_in.model_dump())  # type: ignore
            db.add(db_obj)
            db.flush()
            return db_obj

        except Exception:
            db.rollback()
            raise

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in [ca.key for ca in inspect(db_obj).mapper.column_attrs]:
            if field in update_data and field != "id":
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        return db_obj

    def remove(self, db: Session, *, id: int | List[int]) -> ModelType:
        if isinstance(id, int):
            db.execute(delete(self.model).where(self.model.id == id))
        elif isinstance(id, list):
            db.execute(delete(self.model).where(self.model.id.in_(id)))

    def remove_where(self, db: Session, *, filters: List[dict],
                     model: Optional[Type[ModelType]] = None) -> None:
        mod: ModelType = model if model else self.model
        db.execute(delete(mod).where(*filters))
