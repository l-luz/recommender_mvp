"""
Geração de dados de teste (usuários, livros)
"""

from sqlalchemy.orm import Session
from typing import List

from ..db import models, crud


def seed_users(db: Session, n_users: int = 10):
    """
    Cria usuários de teste.
    
    Args:
        db: Sessão de DB
        n_users: Número de usuários a criar
    """
    for i in range(n_users):
        existing = crud.get_user_by_username(db, f"user_{i}")
        if not existing:
            crud.create_user(
                db,
                username=f"user_{i}",
                password=f"password_{i}"
            )
    print(f"✓ {n_users} usuários criados/verificados")


def seed_books(db: Session, n_books: int = 50):
    """
    Cria livros de teste.
    
    Args:
        db: Sessão de DB
        n_books: Número de livros a criar
    """
    genres = ["Ficção", "Romance", "Mistério", "Sci-Fi", "Fantasia"]
    
    for i in range(n_books):
        existing = db.query(models.Book).filter_by(title=f"Book {i}").first()
        if not existing:
            crud.create_book(
                db,
                title=f"Book {i}",
                authors=f"Author {i % 10}",
                categories=genres[i % len(genres)],
                description=f"Description for book {i}"
            )
    print(f"✓ {n_books} livros criados/verificados")


def seed_database(db: Session):
    """
    Popula o banco com dados iniciais.
    
    Args:
        db: Sessão de DB
    """
    print("Seeding database...")
    seed_users(db, n_users=10)
    seed_books(db, n_books=50)
    print("✓ Database seeded successfully!")
