"""FastAPI slate route tests."""


def test_slate_recommendations_success(client, user_and_books, db_session):
    user, books = user_and_books

    response = client.post(
        "/slate/recommend",
        params={"user_id": user.id, "n_items": 2},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["user_id"] == user.id
    assert payload["total"] == 2
    assert len(payload["recommendations"]) == 2
    returned_ids = {item["book_id"] for item in payload["recommendations"]}
    # All returned books must exist in DB to avoid leaking stale ids
    from app.db import crud

    for book_id in returned_ids:
        assert crud.get_book(db_session, book_id) is not None


def test_slate_invalid_user_returns_404(client):
    response = client.post("/slate/recommend", params={"user_id": 999, "n_items": 1})
    assert response.status_code == 404


def test_slate_404_user(client):
    resp = client.post("/slate/recommend", params={"user_id": 9999, "n_items": 3})
    assert resp.status_code == 404


def test_slate_caps_n_items(client, user_and_books):
    user, books = user_and_books
    resp = client.post("/slate/recommend", params={"user_id": user.id, "n_items": 10})
    data = resp.json()
    assert resp.status_code == 200
    assert len(data["recommendations"]) <= 10
    assert all(
        "authors" in item and "categories" in item and "image" in item
        for item in data["recommendations"]
    )
