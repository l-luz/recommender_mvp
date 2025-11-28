"""
CRUD (Create, Read, Update, Delete) operations in the database
"""

import json
from sqlalchemy.orm import Session, load_only
from typing import List, Optional, Tuple
from sqlalchemy import desc, func

from . import models


# ==================== USER ====================


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


def update_user_genres(db: Session, user_id: int, categories: str) -> models.User:
    """Update user's preferred categories"""
    user = get_user(db, user_id)
    if user:
        setattr(user, "preferred_genres", categories)
        db.commit()
        db.refresh(user)
    return user


def get_user_book_states(db: Session, user_id: int) -> dict:
    """
    Rebuilds the current state of all books with which the user has interacted.
    Returns a dictionary: {book_id: ActionType}
    """

    events = (
        db.query(models.Event)
        .filter(models.Event.user_id == user_id)
        .order_by(models.Event.timestamp.asc())
        .all()
    )

    current_state = {}
    for event in events:
        current_state[event.book_id] = event.action_type

    return current_state


def get_user_liked_books_current(db: Session, user_id: int) -> List[models.Book]:
    """
    Returns ONLY books that are CURRENTLY liked.
    If the user clicked Like -> Clear, this book will NOT appear here.
    """
    states = get_user_book_states(db, user_id)

    liked_ids = [
        bid for bid, action in states.items() if action == models.ActionType.LIKE
    ]

    if not liked_ids:
        return []

    return db.query(models.Book).filter(models.Book.id.in_(liked_ids)).all()


def get_user_disliked_books_current(db: Session, user_id: int) -> List[models.Book]:
    """
    Mesma lógica, mas para Dislikes atuais.
    """
    states = get_user_book_states(db, user_id)

    disliked_ids = [
        bid for bid, action in states.items() if action == models.ActionType.DISLIKE
    ]

    if not disliked_ids:
        return []

    return db.query(models.Book).filter(models.Book.id.in_(disliked_ids)).all()


# ==================== CATEGORY ====================
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


def get_all_categories(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Category]:
    """List all categories"""
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_distinct_categories(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Category]:
    """List distinct categories"""
    return db.query(models.Category).offset(skip).limit(limit).distinct().all()


def get_categories_frequency(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Tuple[models.Category, int]]:
    """List categories frequency"""

    total_books_expr = func.count(models.book_categories.c.book_id).label("total_books")

    results = (
        db.query(models.Category, total_books_expr)
        .join(models.book_categories)
        .group_by(models.Category)
        .order_by(desc(total_books_expr))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [tuple(row) for row in results]


# ==================== AUTHOR ====================


def get_all_authors(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Author]:
    """List all authors"""
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_books_ids(
    db: Session, author_id: int, skip: int = 0, limit: int = 100
) -> List[int]:
    """List all authors"""
    return (
        db.query(models.book_authors)
        .filter(models.book_authors.c.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_or_create_author(db: Session, name: str) -> models.Author:
    """Get existing author by name, or create it if it does't exist"""
    author = db.query(models.Author).filter(models.Author.name == name).first()
    if not author:
        author = models.Author(name=name)
        db.add(author)
        db.commit()
        db.refresh(author)
    return author


def get_authors_frequency(db: Session, skip: int = 0, limit: int = 100):
    total_books_expr = func.count(models.book_authors.c.book_id).label("total_books")

    results = (
        db.query(models.Author, total_books_expr)
        .join(models.book_authors)
        .group_by(models.Author)
        .order_by(desc(total_books_expr))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [tuple(row) for row in results]


def get_publisher_frequency(db: Session, skip: int = 0, limit: int = 100):
    total_books_expr = func.count().label("total_books")  # Conta as linhas

    results = (
        db.query(models.Book.publisher, total_books_expr)
        .filter(models.Book.publisher != None)
        .group_by(models.Book.publisher)
        .order_by(desc(total_books_expr))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [tuple(row) for row in results]


# ==================== BOOK ====================
def create_book(
    db: Session,
    title: str,
    authors: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
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
        categories: Original categories string from CSV
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
        authors=str(authors),
        categories=str(categories),
        description=description,
        image=image,
        info_link=info_link,
        publisher=publisher,
        published_date=published_date,
        ratings_count=ratings_count,
        avg_rating=avg_rating,
        price=price,
    )

    db.add(book)

    # Add categories if provided
    if categories:
        for category_name in categories:
            category = get_or_create_category(db, category_name.strip())
            book.categories_rel.append(category)

    if authors:
        for author_name in authors:
            author = get_or_create_author(db, author_name.strip())
            book.authors_rel.append(author)

    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """Retrieve book by ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """List all books"""
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_all_book_ids(db: Session, skip: int = 0, limit: int = 100) -> List[int]:
    books = (
        db.query(models.Book)
        .options(load_only(models.Book.id))  # type: ignore
        .order_by(models.Book.id)
        .all()
    )
    return [b.id for b in books]  # type: ignore


def get_book_authors_ids(
    db: Session, book_id: int, skip: int = 0, limit: int = 100
) -> List[int]:
    """List all authors"""
    return (
        db.query(models.book_authors)
        .filter(models.book_authors.c.book_id == book_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# ==================== EVENT ====================
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


def count_user_events(db: Session, user_id: int, event: str) -> int:
    """
    Counts of the user like events.
    """

    return (
        db.query(models.Event)
        .filter(
            models.Event.user_id == user_id,
            models.Event.action_type == event,
        )
        .count()
    )


def count_user_unique_book_events(db: Session, user_id: int) -> int:
    """
    Counts the user unique books interacted.
    """
    events = (
        db.query(models.Event)
        .filter(
            models.Event.user_id == user_id,
        )
        .all()
    )

    books = set()
    for event in events:
        books.add(event.book_id)  # type: ignore

    return len(books)


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


# TODO: limit = 1
def get_user_last_book_event(
    db: Session, user_id: int, book_id: int
) -> Optional[models.Event]:
    """Get the most recent event for a user and book"""
    return (
        db.query(models.Event)
        .filter(models.Event.user_id == user_id, models.Event.book_id == book_id)
        .order_by(models.Event.timestamp.desc())
        .first()
    )


def get_user_latest_interactions(
    db: Session, user_id: int, limit: int = 100, skip: int = 0
):
    """Get user latest interactions"""
    return (
        db.query(models.Event)
        .filter(models.Event.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .filter(
            models.Event.action_type.in_(
                [
                    models.ActionType.LIKE,
                    models.ActionType.DISLIKE,
                    models.ActionType.CLEAR,
                ]
            )
        )
        .order_by(models.Event.created_at.desc())
        .all()
    )


def get_user_available_books(
    db: Session, user_id: int, limit: int = 100, skip: int = 0
):
    """Get user available books for interaction"""
    liked_books = get_user_liked_books_current(db, user_id)
    disliked_books = get_user_disliked_books(db, user_id)

    liked_ids = [book.id for book in liked_books]
    disliked_ids = [book.id for book in disliked_books]
    excluded_ids = liked_ids + disliked_ids
    return (
        db.query(models.Book)
        .filter(~models.Book.id.in_(excluded_ids))
        .offset(skip)
        .limit(limit)
        .all()
    )
