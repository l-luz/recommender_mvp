"""Shared pytest fixtures for the project."""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import crud
from app.db.database import Base, get_db
from app.main import app


# ==================== Database fixtures ====================


@pytest.fixture(scope="session")
def test_engine():
    """In-memory SQLite engine shared across connections."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(test_engine):
    """Database session bound to the shared in-memory engine."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(test_engine):
    """FastAPI test client using the in-memory database."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ==================== Data seeding helpers ====================


@pytest.fixture
def user_and_books(db_session):
    """Create one user and a small catalog, and wire ARM_INDEX for feedback tests."""
    username = f"user_{uuid.uuid4().hex[:6]}"
    user = crud.create_user(db_session, username, "secret")

    books = [
        crud.create_book(
            db_session, "Book A", authors=["Author 1"], categories=["Fiction"]
        ),
        crud.create_book(
            db_session, "Book B", authors=["Author 2"], categories=["Fantasy"]
        ),
        crud.create_book(
            db_session, "Book C", authors=["Author 3"], categories=["Sci-Fi"]
        ),
    ]

    # Keep the RL runtime arm index in sync with the test catalog
    from app.core import rl_runtime as rl

    rl.init_runtime(db_session)

    for idx, book in enumerate(books):
        rl.ARM_INDEX[book.id] = idx  # type: ignore

    return user, books
