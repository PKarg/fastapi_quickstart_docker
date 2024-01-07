from requests.auth import HTTPBasicAuth
from sqlalchemy import select

from models.users import User
from run.config import project_settings


def test_create_player_endpoint(get_test_db, prepare_test_client, create_test_user):
    db = get_test_db
    client = prepare_test_client
    players = db.execute(select(User)).scalars().all()
    response = client.post(url="/users",
                           auth=HTTPBasicAuth(username=project_settings.main.docs_username,
                                              password=project_settings.main.docs_password.get_secret_value()),
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
