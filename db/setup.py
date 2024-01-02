from functools import lru_cache

from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base

from run.config import project_settings

from sqlalchemy import URL, create_engine

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=project_settings.postgres.postgres_user,
    password=project_settings.postgres.postgres_password.get_secret_value(),
    host=project_settings.postgres.postgres_host,
    port=project_settings.postgres.pgport,
    database=project_settings.postgres.postgres_db
)

engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeBase = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()


@lru_cache(maxsize=1)
def get_model_registry() -> dict:
    return {m.class_.__tablename__: m.class_ for m in Base.registry.mappers}
