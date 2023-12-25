import datetime
import re

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__
        return re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name).lower() + "s"


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False,
                                                          server_default=func.now(), onupdate=func.now())
