"""
SQLite + SessionLocal connection configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Definir diretório de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
DATABASE_URL = f"sqlite:///{DATA_DIR}/database.db"

# Criar engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()


def get_db():
    """
    Provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Creates all tables in the database.
    """
    Base.metadata.create_all(bind=engine)
