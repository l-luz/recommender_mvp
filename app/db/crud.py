"""
CRUD (Create, Read, Update, Delete) operations in the database
"""

import json
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models


#
# USER
#
def create_user(db: Session, username: str, password: str) -> models.User:
    """Create new user"""
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Recover user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Recover user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def update_user_genres(db: Session, user_id: int, genres: str) -> models.User:
    """Update user's preferred genres"""
    user = get_user(db, user_id)
    if user:
        setattr(user, "preferred_genres", genres)
        db.commit()
        db.refresh(user)
    return user


#
#  CATEGORY
#
def get_or_create_category(db: Session, name: str) -> models.Category:
    """Get existing category by name, or create it if it doesn't exist"""
    category = db.query(models.Category).filter(models.Category.name == name).first()
    if not category:
        category = models.Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """Retrieve category by ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """List all categories"""
    return db.query(models.Category).offset(skip).limit(limit).all()


#
#  BOOK
#
def create_book(
    db: Session,
    title: str,
    authors: Optional[str] = None,
    categories_raw: Optional[str] = None,
    category_names: Optional[List[str]] = None,
    description: Optional[str] = None,
    image: Optional[str] = None,
    info_link: Optional[str] = None,
    publisher: Optional[str] = None,
    published_date: Optional[str] = None,
    ratings_count: int = 0,
    avg_rating: float = 0.0,
    price: Optional[float] = None,
) -> models.Book:
    """
    Create new book with many-to-many category relationship
    
    Args:
        db: Database session
        title: Book title
        authors: Comma-separated author names
        categories_raw: Original categories string from CSV
        category_names: List of category names to associate with this book
        description: Book description
        image: Image URL
        info_link: Info link URL
        publisher: Publisher name
        published_date: Publication date
        ratings_count: Number of ratings
        avg_rating: Average rating score
        price: Book price
    
    Returns:
        Created Book instance with associated categories
    """
    book = models.Book(
        title=title,
        authors=authors,
        categories_raw=categories_raw,
        description=description,
        image=image,
        info_link=info_link,
        publisher=publisher,
        published_date=published_date,
        ratings_count=ratings_count,
        avg_rating=avg_rating,
        price=price,
    )
    
    # Add categories if provided
    if category_names:
        for category_name in category_names:
            category = get_or_create_category(db, category_name.strip())
            book.categories_rel.append(category)
    
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """Retrieve book by ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """List all books"""
    return db.query(models.Book).offset(skip).limit(limit).all()


#
#  EVENT
#
def _reward_from_action(action_type: models.ActionType) -> float:
    """
    Simple reward policy:
    like=1.0, dislike=0.0,
    # TODO: click=0.3, info=0.1
    """
    if action_type == models.ActionType.LIKE:
        return 1.0
    if action_type == models.ActionType.CLEAR:
        return 0.3
    return 0.0


def create_event(
    db: Session,
    user_id: int,
    book_id: int,
    slate_id: str,
    pos: int,
    action_type: str,
    ctx_features: Optional[str] = None,
    reward_w: float = 0.0,
) -> models.Event:
    """Records an event (like, dislike, click)"""
    action_enum = models.ActionType(action_type)
    reward = _reward_from_action(action_enum)

    event = models.Event(
        user_id=user_id,
        book_id=book_id,
        slate_id=slate_id,
        pos=pos,
        action_type=action_enum,
        reward=reward,
        reward_w=reward_w,
        ctx_features=(
            json.dumps(ctx_features) if isinstance(ctx_features, dict) else ctx_features
        ),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_user_events(
    db: Session, user_id: int, action_type: Optional[str] = None
) -> List[models.Event]:
    """List of events for a user"""
    query = db.query(models.Event).filter(models.Event.user_id == user_id)
    if action_type:
        query = query.filter(models.Event.action_type == models.ActionType(action_type))
    return query.all()


def get_events_by_slate(db: Session, slate_id: str) -> List[models.Event]:
    """List all events on a slate (recommendation)"""
    return db.query(models.Event).filter(models.Event.slate_id == slate_id).all()


def update_event_reward(
    db: Session, event_id: int, reward: float, reward_w: float = 0.0
) -> Optional[models.Event]:
    """Update reward for an event"""
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        setattr(event, "reward", reward)
        setattr(event, "reward_w", reward_w)
        db.commit()
        db.refresh(event)
    return event


def get_user_liked_books(db: Session, user_id: int) -> List[models.Book]:
    """List all books liked by a user"""
    liked_events = (
        db.query(models.Event)
        .filter(
            models.Event.user_id == user_id,
            models.Event.action_type == models.ActionType.LIKE,
        )
        .all()
    )

    books: List[models.Book] = []
    for event in liked_events:
        book = get_book(db, event.book_id)  # type: ignore
        if book:
            books.append(book)

    return books


def get_user_disliked_books(db: Session, user_id: int) -> List[models.Book]:
    """List all books disliked by a user"""
    disliked_events = (
        db.query(models.Event)
        .filter(
            models.Event.user_id == user_id,
            models.Event.action_type == models.ActionType.DISLIKE,
        )
        .all()
    )

    books: List[models.Book] = []
    for event in disliked_events:
        book = get_book(db, event.book_id)  # type: ignore
        if book:
            books.append(book)

    return books

def get_user_last_book_event(
    db: Session,
    user_id: int,
    book_id: int
) -> Optional[models.Event]:
    """Get the most recent event for a user and book"""
    return (
        db.query(models.Event)
        .filter(
            models.Event.user_id == user_id,
            models.Event.book_id == book_id
        )
        .order_by(models.Event.timestamp.desc())
        .first()
    )

# def get_user_liked_books_with_events(
#     db: Session,
#     user_id: int
# ) -> List[tuple]:
#     """List all books liked by a user with their event data (book, event)"""
#     liked_events = db.query(models.Event).filter(
#         models.Event.user_id == user_id,
#         models.Event.action_type == models.ActionType.LIKE
#     ).all()

#     books_with_events = []
#     for event in liked_events:
#         book = get_book(db, event.book_id)
#         if book:
#             books_with_events.append((book, event))

#     return books_with_events
