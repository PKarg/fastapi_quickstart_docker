from auth.functions import (create_access_token, get_password_hash,
                            verify_password)


def test_create_access_token():
    assert create_access_token("dev", 1)


def test_get_password_hash():
    assert get_password_hash("dev")


def test_verify_password():
    password_hash = get_password_hash("dev")
    assert verify_password("dev", password_hash)
    assert not verify_password("test123", password_hash)
