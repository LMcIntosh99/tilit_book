from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = URL.create(
    "postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host="localhost",
    port=5432,
    database=DATABASE,
)

engine = create_engine(DATABASE_URL)
os.environ["DATABASE_URL"] = engine.url.render_as_string(hide_password=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
