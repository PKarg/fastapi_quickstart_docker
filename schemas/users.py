import datetime
from typing import Optional

from email_validator import validate_email
from pydantic import BaseModel, field_validator, model_validator, Field, ConfigDict


# TODO user updating should be implemented separately

class UserBaseSchema(BaseModel):
    username: str = Field(description="User username.", max_length=30, min_length=5)
    email_address: Optional[str] = Field(None, max_length=50)
    created_at: Optional[datetime.datetime] = Field(datetime.datetime.now(),
                                                    description="Time when player was added to the database.")
    status: Optional[int] = Field(0, description="User status.", ge=0, le=2)
    auth_level: Optional[int] = Field(0, description="User authorization level.", ge=0, le=2)
    identifier: Optional[str] = Field(None, description="User unique identifier.", max_length=12)
    language_code: str = Field("en", description="User language code.", max_length=8)

    @field_validator("email_address")
    def validate_player_mail(cls, v: str) -> str | None:
        if v:
            validate_email(v)
        return v


class UserCreateSchema(UserBaseSchema):
    raw_password: str = Field(description="User password.", max_length=30, min_length=8)


class UserCreateSchemaHashed(UserBaseSchema):
    model_config = ConfigDict(extra="ignore")

    hashed_password: str = Field(max_length=128, min_length=32)


class UserFilterSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = Field(None, description="User ID.", ge=1)
    name: Optional[str] = Field(None, description="User username.", max_length=30, min_length=5)
    time_added: Optional[datetime.datetime] = Field(None, description="Time when player was added to the database.")
    identifier: Optional[str] = Field(None, description="User unique identifier.", max_length=12)
