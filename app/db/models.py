"""
Models SQLAlchemy: User, Book, ActionType, Event
"""

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Table,
)
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import enum
import ast
from .database import Base
from typing import List, Optional


# Association tables for many-to-many relationships
book_categories = Table(
    "book_categories",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)

book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
)


class Category(Base):
    """Book categories/genre table"""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship to books (many-to-many)
    books = relationship(
        "Book", secondary=book_categories, back_populates="categories_rel"
    )


class Author(Base):
    """Book authors table"""

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship to books (many-to-many)
    books = relationship("Book", secondary=book_authors, back_populates="authors_rel")


class User(Base):
    """User table"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(Text)  # Password hash
    preferred_genres = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))

    # Relationship
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")

    @property
    def get_genre_list(self):
        return self._get_list_field("preferred_genres")

    def _get_list_field(self, column_name: str) -> List[str]:
        """
        Returns the field value as a list.
        If it is None, an empty string, or a list string, returns an empty list.
        """
        value = getattr(self, column_name, None)
        if not value:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return parsed
                return []
            except Exception:
                return []
        return []


class Book(Base):
    """Book table"""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    authors = Column(Text, nullable=True)  # Comma-separated
    categories = Column(Text, nullable=True)  # Original CSV categories as string
    description = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    info_link = Column(Text, nullable=True)
    publisher = Column(Text, nullable=True)
    published_date = Column(String, nullable=True)
    ratings_count = Column(Integer, default=0)
    avg_rating = Column(Float, default=0.0)
    price = Column(Float, nullable=True)

    # Many-to-many relationship
    categories_rel = relationship(
        "Category", secondary=book_categories, back_populates="books"
    )

    authors_rel = relationship("Author", secondary=book_authors, back_populates="books")

    # One to Many relationship
    events = relationship("Event", back_populates="book", cascade="all, delete-orphan")

    @property
    def get_image(self) -> Optional[str]:
        """
        Returns the image URL or None if not available.
        """
        value = getattr(self, "image", None)
        return value if value and value != "None" else None

    @property
    def get_categories_list(self) -> List[str]:
        return self._get_list_field("categories")

    @property
    def get_authors_list(self) -> List[str]:
        return self._get_list_field("authors")

    def _get_list_field(self, column_name: str) -> List[str]:
        """
        Returns the field value as a list.
        If it is None, an empty string, or a list string, returns an empty list.
        """
        value = getattr(self, column_name, None)
        if not value:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return parsed
                return []
            except Exception:
                return []
        return []


class ActionType(str, enum.Enum):
    """Types of events"""

    LIKE = "like"  # positive feedback
    DISLIKE = "dislike"  # negative feedback
    CLEAR = "clear"  # feedback removed


class Event(Base):
    """Table of events (recommendations + feedback)"""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    slate_id = Column(String, index=True, nullable=False)  # Recommendation list ID
    pos = Column(Integer, nullable=False)  # 1..K
    action_type = Column(Enum(ActionType))
    reward = Column(Float, default=0.0)
    reward_w = Column(Float, default=0.0)  # weight-adjusted reward
    ctx_features = Column(String, nullable=True)  # JSON
    timestamp = Column(DateTime, default=datetime.now(UTC), index=True)

    # Relationship
    user = relationship("User", back_populates="events")
    book = relationship("Book", back_populates="events")
