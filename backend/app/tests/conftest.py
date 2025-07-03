# tests/conftest.py

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base
from .. import models
from .. import database as db_module
from ..schemas import CommentCreate
from .. import crud

@pytest.fixture(scope="session")
def db_engine():
    db_url = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/testdb")

    engine = create_engine(db_url)
    db_module.engine = engine
    db_module.SessionLocal = sessionmaker(bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    SessionTesting = sessionmaker(bind=db_engine)
    db = SessionTesting()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    from ..main import app
    from ..routers import comments

    def override_get_db():
        yield db_session

    app.dependency_overrides[comments.get_db] = override_get_db

    from fastapi.testclient import TestClient
    return TestClient(app)
