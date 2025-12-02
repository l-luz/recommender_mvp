"""FastAPI user route tests."""


def test_root_endpoint(client):
    """Tests if the API root endpoint is working correctly."""
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Recommender MVP API"
    assert payload["docs"] == "/docs"


def test_user_registration_and_login_flow(client):
    """Tests the full user registration and login sequence."""
    reg = client.post(
        "/users/register", json={"username": "api_user", "password": "secret"}
    )
    assert reg.status_code == 200
    user_id = reg.json()["event_id"]

    login = client.post(
        "/users/login", json={"username": "api_user", "password": "secret"}
    )
    assert login.status_code == 200
    assert login.json()["event_id"] == user_id

    bad_login = client.post(
        "/users/login", json={"username": "api_user", "password": "wrong"}
    )
    assert bad_login.status_code == 401


def test_register_user_conflict(client, db_session):
    """Ensures registering a user with a duplicate username fails."""
    client.post("/users/register", json={"username": "dup", "password": "x"})
    resp = client.post("/users/register", json={"username": "dup", "password": "x"})
    assert resp.status_code == 400


def test_login_invalid_user(client):
    """Tests login failure for a non-existent user."""
    resp = client.post("/users/login", json={"username": "ghost", "password": "x"})
    assert resp.status_code == 401


def test_profile_not_found(client):
    """Checks if fetching a non-existent user profile returns 404."""
    resp = client.get("/users/profile/9999")
    assert resp.status_code == 404


def test_profile_update_empty_genres(client):
    """Tests updating a user profile with an empty list of genres."""
    reg = client.post("/users/register", json={"username": "nog", "password": "pw"})
    user_id = reg.json()["event_id"]
    resp = client.put(
        f"/users/profile/{user_id}",
        json={"id": user_id, "username": "nog", "preferred_genres": []},
    )
    assert resp.status_code == 200


def test_get_genres(client):
    """Checks if the genres endpoint returns the list of categories."""
    resp = client.get("/users/genres")
    assert resp.status_code == 200
    assert "categories" in resp.json()


def test_profile_update_and_retrieval(client):
    """Tests updating and then retrieving a user profile."""
    reg = client.post(
        "/users/register", json={"username": "profile_user", "password": "secret"}
    )
    user_id = reg.json()["event_id"]

    update = client.put(
        f"/users/profile/{user_id}",
        json={
            "id": user_id,
            "username": "profile_user",
            "preferred_genres": ["Fiction", "Drama"],
        },
    )
    assert update.status_code == 200

    profile = client.get(f"/users/profile/{user_id}")
    assert profile.status_code == 200
    profile_data = profile.json()
    assert profile_data["id"] == user_id
    assert profile_data["preferred_genres"] == ["Fiction", "Drama"]
