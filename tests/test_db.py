"""
Testes do banco de dados
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db import models, crud


@pytest.fixture
def test_db():
    """Fixture: cria banco de testes in-memory"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


class TestUserCRUD:
    """Testes CRUD de usuários"""
    
    def test_create_user(self, test_db):
        """Testa criação de usuário"""
        user = crud.create_user(test_db, "test_user", "password_hash")
        
        assert user.id is not None
        assert user.username == "test_user"
    
    def test_get_user(self, test_db):
        """Testa recuperação de usuário"""
        created = crud.create_user(test_db, "test_user", "password_hash")
        retrieved = crud.get_user(test_db, created.id)
        
        assert retrieved.username == "test_user"
    
    def test_get_user_by_username(self, test_db):
        """Testa busca de usuário por username"""
        created = crud.create_user(test_db, "test_user", "password_hash")
        retrieved = crud.get_user_by_username(test_db, "test_user")
        
        assert retrieved.id == created.id


class TestBookCRUD:
    """Testes CRUD de livros"""
    
    def test_create_book(self, test_db):
        """Testa criação de livro"""
        book = crud.create_book(
            test_db,
            "Test Book",
            "Test Author",
            "Fiction",
            "Test description"
        )
        
        assert book.id is not None
        assert book.title == "Test Book"
    
    def test_get_book(self, test_db):
        """Testa recuperação de livro"""
        created = crud.create_book(
            test_db,
            "Test Book",
            "Test Author",
            "Fiction",
            "Test description"
        )
        retrieved = crud.get_book(test_db, created.id)
        
        assert retrieved.title == "Test Book"
    
    def test_get_all_books(self, test_db):
        """Testa listagem de livros"""
        for i in range(5):
            crud.create_book(test_db, f"Book {i}", "Author", "Genre", "Desc")
        
        books = crud.get_all_books(test_db, limit=100)
        assert len(books) == 5


class TestEventCRUD:
    """Testes CRUD de eventos"""
    
    def test_create_event(self, test_db):
        """Testa criação de evento"""
        user = crud.create_user(test_db, "user1", "hash")
        book = crud.create_book(test_db, "Book", "Author", "Genre", "Desc")
        
        event = crud.create_event(
            test_db,
            user.id,
            book.id,
            "like",
            reward=1.0
        )
        
        assert event.user_id == user.id
        assert event.book_id == book.id
    
    def test_get_user_events(self, test_db):
        """Testa recuperação de eventos do usuário"""
        user = crud.create_user(test_db, "user1", "hash")
        book = crud.create_book(test_db, "Book", "Author", "Genre", "Desc")
        
        crud.create_event(test_db, user.id, book.id, "like", 1.0)
        crud.create_event(test_db, user.id, book.id, "dislike", 0.0)
        
        events = crud.get_user_events(test_db, user.id)
        assert len(events) == 2
