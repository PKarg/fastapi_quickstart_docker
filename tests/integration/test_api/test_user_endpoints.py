from requests.auth import HTTPBasicAuth
from sqlalchemy import select

from models.users import User


def test_create_player_endpoint(get_test_db, prepare_test_client, create_test_user):
    db = get_test_db
    client = prepare_test_client
    players = db.execute(select(User)).scalars().all()
    response = client.post(url="/users", auth=HTTPBasicAuth(username="testadmin", password="testadmin"),
                           json={"username": "user123",
                                 "raw_password": "pass134567",
                                 "email_address": "test_user@test.com"})
    assert response.status_code == 201


def test_get_token_endpoint(get_test_db, prepare_test_client, create_test_user):
    db = get_test_db
    client = prepare_test_client
    response = client.post(url="/users/auth/token", data={"username": "testUser",
                                                          "password": "testPassword"})
    assert response.status_code == 200
    assert response.json()["access_token"]
