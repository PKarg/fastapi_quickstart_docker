from crud.users import user_crud
from schemas.users import UserCreateSchema


def test_create_user(get_test_db):
    db = get_test_db
    user_data = UserCreateSchema(username="testuser", raw_password="password", email_address="dev@dev.com",
                                 language_code="en")

    result = user_crud.create_user(db, user_data, "hashed_password" * 3)
    db.add(result)
    db.commit()
    db.refresh(result)
    assert result.username == "testuser"
    assert result.hashed_password == "hashed_password" * 3
