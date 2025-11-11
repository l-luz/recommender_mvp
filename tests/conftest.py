"""
Fixtures e configurações para testes
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base


@pytest.fixture(scope="session")
def test_db_engine():
    """Cria engine de teste in-memory"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def test_db(test_db_engine):
    """Cria sessão de teste"""
    TestingSessionLocal = sessionmaker(bind=test_db_engine)
    db = TestingSessionLocal()
    yield db
    db.close()
