# tests/conftest.py

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base
from .. import models
from .. import database as db_module


@pytest.fixture(scope="function")
def db_engine():
    db_url = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/testdb")

    # Try PostgreSQL first, fall back to SQLite for local development
    try:
        engine = create_engine(db_url)
        # Test the connection
        with engine.connect() as conn:
            pass
        print(f"Using PostgreSQL database: {db_url}")
    except Exception as e:
        print(f"PostgreSQL not available ({e}), falling back to SQLite for local testing")
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

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
def client(db_session, db_engine):
    from ..main import app
    from ..routers import comments
    from .. import database as db_module

    # Override the get_engine function BEFORE creating TestClient
    # This ensures the startup event uses our test engine
    original_get_engine = db_module.get_engine
    db_module.get_engine = lambda: db_engine

    def override_get_db():
        yield db_session

    # Override the database dependency
    app.dependency_overrides[comments.get_db] = override_get_db

    from fastapi.testclient import TestClient
    client = TestClient(app)

    yield client

    # Clean up overrides
    app.dependency_overrides.clear()
    db_module.get_engine = original_get_engine
