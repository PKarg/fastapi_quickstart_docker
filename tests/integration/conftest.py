import pytest
from sqlalchemy import event, create_engine, URL, Engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from auth.functions import get_password_hash
from crud.users import user_crud
from db.setup import Base, get_db
from main import app
from run.config import project_settings
from schemas.users import UserCreateSchema

test_db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=project_settings.postgres.postgres_user,
    password=project_settings.postgres.postgres_password.get_secret_value(),
    host=project_settings.postgres.postgres_host,
    port=project_settings.postgres.pgport,
    database=project_settings.postgres.postgres_db
)

test_engine: Engine = create_engine(test_db_url,
                                    echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@event.listens_for(test_engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


@event.listens_for(test_engine, "begin")
def do_begin(conn):
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")


@pytest.fixture(scope="session")
def get_project_settings():
    yield project_settings


@pytest.fixture(scope="session")
def prepare_test_tables():
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def get_test_db(prepare_test_tables):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(sess, trans):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def create_test_user(get_test_db):
    db: Session = get_test_db
    u_data = UserCreateSchema(username="testUser",
                              raw_password="testPassword",
                              email_address="test@test.com",
                              status=1)
    hashed_password = get_password_hash(u_data.raw_password)
    user = user_crud.create_user(db=db, user_data=u_data,
                                 hashed_password=hashed_password)
    db.add(user)
    db.commit()
    yield user


@pytest.fixture
def prepare_test_client(get_test_db):
    def override_get_db():
        yield get_test_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
