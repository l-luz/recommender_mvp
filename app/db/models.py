"""
Models SQLAlchemy: User, Book, ActionType, Event
"""

from sqlalchemy import Column, Integer, Text, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base


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
    title = Column(String, nullable=False)
    authors = Column(Text, nullable=True)  # Comma-separated
    categories = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    info_link = Column(Text, nullable=True)
    publisher = Column(Text, nullable=True)
    published_date = Column(String, nullable=True)
    ratings_count = Column(Integer, default=0)
    avg_rating = Column(Float, default=0.0)
    price = Column(Float, nullable=True)

    # Relationship
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
