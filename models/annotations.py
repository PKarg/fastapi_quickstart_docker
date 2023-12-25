from typing import Annotated

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column

int_pk = Annotated[
    int,
    mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
]

user_id_fk = Annotated[
    int,
    mapped_column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
]
