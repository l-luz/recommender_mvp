"""
Rotas /users -> autenticação, registro e perfil de usuário
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud, database
from app.api import schemas
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])


# ==================== Endpoints ====================


@router.post("/register", response_model=schemas.FeedbackResponse)
def register_user(
    user_data: schemas.LoginRequest, db: Session = Depends(database.get_db)
) -> schemas.FeedbackResponse:
    """
    Registers a new user.

    Args:
        user_data: LoginRequest with username and password
        db: Database session

    Returns:
        FeedbackResponse confirming registration

    Raises:
        HTTPException: If user already exists
    """
    existing_user = crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400, detail=f"User '{user_data.username}' already exists"
        )

    try:
        password_bytes = user_data.password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        hashed_string = hashed_bytes.decode("utf-8")

        user = crud.create_user(
            db=db, username=user_data.username, password=hashed_string
        )

        return schemas.FeedbackResponse(
            success=True,
            message=f"User '{user_data.username}' registered successfully",
            event_id=user.id,  # type: ignore
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")


@router.post("/login", response_model=schemas.FeedbackResponse)
def login_user(
    credentials: schemas.LoginRequest, db: Session = Depends(database.get_db)
) -> schemas.FeedbackResponse:
    """
    Authenticates a user.

    Args:
        credentials: LoginRequest with username and password
        db: Database session

    Returns:
        FeedbackResponse with user_id

    Throws:
        HTTPException: If credentials are invalid
    """
    user = crud.get_user_by_username(db, credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    password_bytes = credentials.password.encode("utf-8")

    if not bcrypt.checkpw(password_bytes, user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return schemas.FeedbackResponse(
        success=True,
        message=f"User '{credentials.username}' logged in successfully",
        event_id=user.id,  # type: ignore
    )


@router.get("/profile/{user_id}", response_model=schemas.HistorySummary)
def get_profile(user_id: int, db: Session = Depends(database.get_db)) -> dict:
    """
    Returns user profile.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        Dict with user data
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    genres_list = []
    if str(user.preferred_genres):
        genres_list = user.preferred_genres.split(",")
    likes = crud.count_user_events(db, user.id, schemas.ActionType.LIKE)  # type: ignore
    dislikes = crud.count_user_events(db, user.id, schemas.ActionType.DISLIKE)  # type: ignore
    cleaneds = crud.count_user_events(db, user.id, schemas.ActionType.CLEAR)  # type: ignore

    try:
        return {
            "id": user.id,
            "username": user.username,
            "preferred_genres": genres_list,
            "total_events": likes + dislikes + cleaneds,
            "likes": likes,
            "dislikes": dislikes,
            "unique_books_interacted": crud.count_user_unique_book_events(db, user_id),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving categoriessssssssssss: {str(e)}"
        )


@router.put("/profile/{user_id}", response_model=schemas.FeedbackResponse)
def update_profile(
    user_id: int,
    profile_data: schemas.UserBase,
    db: Session = Depends(database.get_db),
) -> schemas.FeedbackResponse:
    """
    Updates user profile.

    Args:
        user_id: User ID
        profile_data: UserBase with updated data
        db: Database session

    Returns:
        FeedbackResponse confirming update
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    try:
        if profile_data.preferred_genres:
            crud.update_user_genres(
                db, user_id, ",".join(profile_data.preferred_genres)
            )

        return schemas.FeedbackResponse(
            success=True,
            message=f"User '{user.username}' profile updated successfully",
            event_id=user_id,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {str(e)}")


@router.get("/genres", response_model=schemas.CategoryList)
def get_genre_options(
    db: Session = Depends(database.get_db),
) -> schemas.CategoryList:
    """Returns available genres options
    Args:
        db: Database session
    Returns:
        List of genres
    """
    categories = crud.get_all_categories(db)
    genre_strings: list[str] = [str(genre.name) for genre in categories]

    try:
        return schemas.CategoryList(categories=genre_strings)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving categories: {str(e)}"
        )
