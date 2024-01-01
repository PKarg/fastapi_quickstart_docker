import pytest
from sqlalchemy import event, create_engine, URL, Engine
from sqlalchemy.orm import sessionmaker

from db.setup import Base
from run.config import project_settings

test_db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=project_settings.postgres_settings.postgres_user,
    password=project_settings.postgres_settings.postgres_password.get_secret_value(),
    host=project_settings.postgres_settings.postgres_host,
    port=project_settings.postgres_settings.pgport,
    database=project_settings.postgres_settings.postgres_db
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
