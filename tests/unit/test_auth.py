from auth.functions import (create_access_token, get_password_hash,
                            verify_password, create_user_identifier)


def test_create_access_token():
    assert create_access_token("test", 1)


def test_get_password_hash():
    assert get_password_hash("test")


def test_verify_password():
    password_hash = get_password_hash("test")
    assert verify_password("test", password_hash)
    assert not verify_password("test123", password_hash)


def test_create_user_identifier():
    assert create_user_identifier()
