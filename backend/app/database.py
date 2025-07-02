"""
Database setup module.

Loads environment variables for DB credentials, configures the SQLAlchemy engine,
session factory, and base class for ORM models.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = URL.create(
    "postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(DB_URL)
os.environ["DB_URL"] = engine.url.render_as_string(hide_password=False)
SessionLocal = sessionmaker(bind=engine)

# Base class for declarative ORM models to inherit from
Base = declarative_base()
