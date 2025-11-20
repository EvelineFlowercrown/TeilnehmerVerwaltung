# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///Database.db"

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)  # sqlite-threadsafety
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
SessionLocal = SessionLocal()


class BaseClass(DeclarativeBase):
    pass
