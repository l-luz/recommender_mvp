"""FastAPI feedback route tests."""

from app.db import crud, models


def test_feedback_register_like(client, user_and_books, db_session):
    """Tests registering a 'like' event and verifies it's saved to the DB."""
    user, books = user_and_books
    target_book = books[0]

    response = client.post(
        "/feedback/register",
        json={
            "user_id": user.id,
            "book_id": target_book.id,
            "action_type": "like",
            "slate_id": "slate-test",
            "pos": 1,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["event_id"] is not None

    events = crud.get_user_events(db_session, user.id)
    assert any(
        evt.book_id == target_book.id and evt.action_type == models.ActionType.LIKE
        for evt in events
    )


def test_feedback_user_not_found(client):
    """Checks if registering feedback for a non-existent user returns 404."""
    resp = client.post(
        "/feedback/register",
        json={
            "user_id": 999,
            "book_id": 1,
            "action_type": "like",
            "slate_id": "",
            "pos": 1,
        },
    )
    assert resp.status_code == 404


def test_feedback_book_not_found(client):
    """Checks if registering feedback for a non-existent book returns 404."""
    reg = client.post("/users/register", json={"username": "fb", "password": "pw"})
    user_id = reg.json()["event_id"]
    resp = client.post(
        "/feedback/register",
        json={
            "user_id": user_id,
            "book_id": 9999,
            "action_type": "like",
            "slate_id": "",
            "pos": 1,
        },
    )
    assert resp.status_code == 404


def test_feedback_dislike_and_history(client, user_and_books):
    """Tests registering a 'dislike' and then querying the user's history."""
    user, books = user_and_books
    client.post(
        "/feedback/register",
        json={
            "user_id": user.id,
            "book_id": books[0].id,
            "action_type": "dislike",
            "slate_id": "s1",
            "pos": 1,
        },
    )
    hist = client.get(f"/feedback/user/{user.id}/history")
    data = hist.json()

    assert (
        data["dislikes"] == 1
        and data["likes"] == 0
        and data["total_events"] == 1
        and data["unique_books_interacted"] == 1
    )

def test_feedback_like_and_history(client, user_and_books):
    """Tests registering a 'like' and then querying the user's history."""
    user, books = user_and_books
    client.post(
        "/feedback/register",
        json={
            "user_id": user.id,
            "book_id": books[0].id,
            "action_type": "like",
            "slate_id": "s1",
            "pos": 1,
        },
    )
    hist = client.get(f"/feedback/user/{user.id}/history")
    data = hist.json()
    assert (
        data["dislikes"] == 0
        and data["likes"] == 1
        and data["total_events"] == 1
        and data["unique_books_interacted"] == 1
    )

def test_feedback_clear_and_history(client, user_and_books):
    """Tests registering a 'clear' event and its impact on history."""
    user, books = user_and_books
    client.post(
        "/feedback/register",
        json={
            "user_id": user.id,
            "book_id": books[0].id,
            "action_type": "like",
            "slate_id": "s1",
            "pos": 1,
        },
    )

    client.post(
        "/feedback/register",
        json={
            "user_id": user.id,
            "book_id": books[0].id,
            "action_type": "clear",
        },
    )
    hist = client.get(f"/feedback/user/{user.id}/history")
    data = hist.json()
    assert (
        data["dislikes"] == 0
        and data["likes"] == 1
        and data["total_events"] == 2
        and data["unique_books_interacted"] == 1
    )


def test_feedback_likes_dislikes_lists(client, user_and_books):
    """Verifies that the user's lists of 'likes' and 'dislikes' are returned correctly."""
    user, books = user_and_books
    client.post(
        "/feedback/register",
        json={
            "user_id": user.id,
            "book_id": books[0].id,
            "action_type": "like",
            "slate_id": "s1",
            "pos": 1,
        },
    )
    client.post(
        "/feedback/register",
        json={
            "user_id": user.id,
            "book_id": books[1].id,
            "action_type": "dislike",
            "slate_id": "s1",
            "pos": 2,
        },
    )
    likes = client.get(f"/feedback/user/{user.id}/likes").json()
    dislikes = client.get(f"/feedback/user/{user.id}/dislikes").json()
    assert likes["total"] == 1 and dislikes["total"] == 1
