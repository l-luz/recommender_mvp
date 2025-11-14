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
from datetime import datetime
import enum

from .database import Base


# Association table for many-to-many relationship between Book and Category
book_categories = Table(
    "book_categories",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)


class Category(Base):
    """Book categories/genres table"""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship to books (many-to-many)
    books = relationship(
        "Book", secondary=book_categories, back_populates="categories_rel"
    )


class User(Base):
    """User table"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Password hash
    preferred_genres = Column(Text, nullable=True)  # comma-separated
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")


class Book(Base):
    """Book table"""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    authors = Column(Text, nullable=True)  # Comma-separated
    categories_raw = Column(Text, nullable=True)  # Original CSV categories as string
    description = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    info_link = Column(Text, nullable=True)
    publisher = Column(Text, nullable=True)
    published_date = Column(String, nullable=True)
    ratings_count = Column(Integer, default=0)
    avg_rating = Column(Float, default=0.0)
    price = Column(Float, nullable=True)

    # Relationship to categories (many-to-many)
    categories_rel = relationship(
        "Category", secondary=book_categories, back_populates="books"
    )

    # Relationship to events
    events = relationship("Event", back_populates="book", cascade="all, delete-orphan")


class ActionType(str, enum.Enum):
    """Types of events"""

    LIKE = "like"  # positive feedback
    DISLIKE = "dislike"  # negative feedback
    # CLICK = "click"  # explicit feedback
    # What is the relevance? user clicked to see more but did not like or dislike... Or he can also give like/dislike after click


class Event(Base):
    """Table of events (recommendations + feedback)"""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    slate_id = Column(String, index=True, nullable=False)  # Recommendation list ID
    pos = Column(Integer, nullable=False)  # 1..K
    action_type = Column(Enum(ActionType))
    reward = Column(Float, default=0.0)  # 0 | 0.5 | 1 dislike|click|like
    reward_w = Column(Float, default=0.0)  # weight-adjusted reward
    ctx_features = Column(String, nullable=True)  # JSON
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationship
    user = relationship("User", back_populates="events")
    book = relationship("Book", back_populates="events")
