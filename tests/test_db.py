"""Database CRUD helpers tests."""

from app.db import crud, models


def test_create_and_get_user(db_session):
    """Tests the creation and retrieval of a user."""
    user = crud.create_user(db_session, "bob", "pw123")

    fetched = crud.get_user(db_session, user.id)
    assert fetched is not None
    assert fetched.username == "bob"
    assert fetched.password == "pw123"


def test_update_user_genres(db_session):
    """Tests updating a user's preferred genres."""
    user = crud.create_user(db_session, "carol", "pw123")

    updated = crud.update_user_genres(db_session, user.id, "fantasy,scifi")
    assert updated is not None
    assert updated.preferred_genres == "fantasy,scifi"

    persisted = crud.get_user(db_session, user.id)
    assert persisted.preferred_genres == "fantasy,scifi"


def test_create_book_with_relations(db_session):
    """Tests creating a book and its relations (authors, categories)."""
    book = crud.create_book(
        db_session,
        "Sample Book",
        authors=["Author 1", "Author 2"],
        categories=["Drama", "Mystery"],
        description="Desc",
    )

    assert book.id is not None
    assert len(book.categories_rel) == 2
    assert len(book.authors_rel) == 2
    assert set(book.get_categories_list) == {"Drama", "Mystery"}
    assert set(book.get_authors_list) == {"Author 1", "Author 2"}


def test_event_states_and_current_lists(db_session):
    """Checks book states (like/dislike/clear) and current feedback lists."""
    user = crud.create_user(db_session, "dave", "pw123")
    like_book = crud.create_book(
        db_session, "Like Book", authors=["A"], categories=["Fiction"]
    )
    dislike_book = crud.create_book(
        db_session, "Dislike Book", authors=["B"], categories=["Horror"]
    )

    crud.create_event(
        db_session,
        user.id,
        like_book.id,
        "slate-1",
        pos=1,
        action_type=models.ActionType.LIKE.value,
    )
    crud.create_event(
        db_session,
        user.id,
        dislike_book.id,
        "slate-1",
        pos=2,
        action_type=models.ActionType.DISLIKE.value,
    )
    crud.create_event(
        db_session,
        user.id,
        like_book.id,
        "slate-1",
        pos=1,
        action_type=models.ActionType.CLEAR.value,
    )

    states = crud.get_user_book_states(db_session, user.id)
    assert states[like_book.id] == models.ActionType.CLEAR
    assert states[dislike_book.id] == models.ActionType.DISLIKE

    liked_now = crud.get_user_liked_books_current(db_session, user.id)
    assert [book.id for book in liked_now] == []

    disliked_now = crud.get_user_disliked_books_current(db_session, user.id)
    assert [book.id for book in disliked_now] == [dislike_book.id]


def test_available_books_excludes_feedback(db_session):
    """Ensures books with feedback do not appear in the available books list."""
    user = crud.create_user(db_session, "eve", "pw123")
    fresh_book = crud.create_book(db_session, "Fresh", authors=["AA"], categories=["X"])
    liked_book = crud.create_book(db_session, "Liked", authors=["BB"], categories=["Y"])

    crud.create_event(
        db_session,
        user.id,
        liked_book.id,
        "slate-2",
        pos=1,
        action_type=models.ActionType.LIKE.value,
    )
    available = crud.get_user_available_books(db_session, user.id)
    available_ids = {book.id for book in available}

    assert fresh_book.id in available_ids
    assert liked_book.id not in available_ids


def test_get_user_by_username(db_session):
    """Tests fetching a user by their username."""
    crud.create_user(db_session, "alice", "pw")
    user = crud.get_user_by_username(db_session, "alice")
    assert user and user.username == "alice"


def test_create_event_with_ctx_features(db_session):
    """Tests creating a feedback event with associated context features."""
    user = crud.create_user(db_session, "ctx", "pw")
    book = crud.create_book(
        db_session, "B", authors=["A"], categories=["C"], description="d"
    )
    evt = crud.create_event(
        db_session,
        user.id,
        book.id,
        "s",
        pos=0,
        action_type=models.ActionType.LIKE.value,
        reward_w=1.0,
        ctx_features="[0.1, 0.2]",
    )
    assert evt.ctx_features == "[0.1, 0.2]"
