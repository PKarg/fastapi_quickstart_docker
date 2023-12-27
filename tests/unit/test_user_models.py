import hashlib
import datetime

import pytest

from models.users import User


def get_player_id_hash():
    return hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).hexdigest()[0:10]


def get_test_hashed_password():
    return hashlib.sha256("testpassword".encode("utf-8")).hexdigest()[0:32]


@pytest.mark.parametrize("username, email_address, hashed_password, identifier",
                         [
                             ("testuser", "test@test.com", get_test_hashed_password(), get_player_id_hash()),
                         ])
def test_player_model(username, email_address, hashed_password, identifier):
    user = User(username=username, email_address=email_address, hashed_password=hashed_password, identifier=identifier)
    assert user
