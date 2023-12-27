from sqlalchemy.orm import Session

from crud.users import user_crud
from schemas.users import UserCreateSchema


def test_create_user(get_test_db):
    user_data = UserCreateSchema(name="test", raw_password="password", email_address="test@test.com",
                                 language_code="en")

    result = user_crud.create_user(get_test_db, user_data, "identifier", "hashed_password")

    assert result.username == "testuser"
    assert result.hashed_password == "hashed_password"
