import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.user import UserBaseSchema, UserCreateSchema, UserCreateSchemaHashed, UserFilterSchema


def test_user_base_schema():
    # Test with valid data
    valid_data = {
        "name": "testuser",
        "email_address": "testuser@test.com",
        "status": 1,
        "auth_level": 0,
        "identifier": "test123"
    }
    user = UserBaseSchema(**valid_data)
    assert user

    # Test with invalid email
    with pytest.raises(ValidationError):
        UserBaseSchema(**{**valid_data, "email_address": "invalid_email"})

    # Test with invalid status
    with pytest.raises(ValidationError):
        UserBaseSchema(**{**valid_data, "status": 3})

    # Test with invalid auth_level
    with pytest.raises(ValidationError):
        UserBaseSchema(**{**valid_data, "auth_level": 3})


def test_user_create_schema():
    # Test with valid data
    valid_data = {
        "name": "testuser",
        "email_address": "testuser@test.com",
        "raw_password": "password123",
        "status": 1,
        "auth_level": 0,
        "identifier": "test123"
    }
    user = UserCreateSchema(**valid_data)
    assert user

    # Test with invalid password
    with pytest.raises(ValidationError):
        UserCreateSchema(**{**valid_data, "raw_password": "short"})


def test_user_create_schema_hashed():
    # Test with valid data
    valid_data = {
        "name": "testuser",
        "email_address": "testuser@test.com",
        "hashed_password": "yxz" * 12,
        "status": 1,
        "auth_level": 0,
        "identifier": "test123"
    }
    user = UserCreateSchemaHashed(**valid_data)
    assert user

    # Test with invalid hashed_password
    with pytest.raises(ValidationError):
        UserCreateSchemaHashed(**{**valid_data, "hashed_password": "short"})


def test_user_filter_schema():
    # Test with valid data
    valid_data = {
        "id": 1,
        "name": "testuser",
        "time_added": datetime.now(),
        "identifier": "test123"
    }
    user = UserFilterSchema(**valid_data)
    assert user

    # Test with invalid id
    with pytest.raises(ValidationError):
        UserFilterSchema(**{**valid_data, "id": 0})
