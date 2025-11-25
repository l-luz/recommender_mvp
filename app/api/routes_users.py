"""
Rotas /users -> autenticação, registro e perfil de usuário
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud, database
from app.api import schemas


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
        user = crud.create_user(
            db=db, username=user_data.username, password=user_data.password
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

    # TODO: use hashing bcrypt
    if user.password != credentials.password:  # type: ignore
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return schemas.FeedbackResponse(
        success=True,
        message=f"User '{credentials.username}' logged in successfully",
        event_id=user.id,  # type: ignore
    )


@router.get("/profile/{user_id}", response_model=schemas.UserBase)
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
    if user.preferred_genres:  # type: ignore
        genres_list = user.preferred_genres.split(",")

    return {
        "id": user.id,
        "username": user.username,
        "preferred_genres": genres_list,
    }


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


@router.get("/genres", response_model=schemas.GenresList)
def get_genre_options(
    db: Session = Depends(database.get_db),
) -> schemas.GenresList:
    """Returns available genres options
    Args:
        db: Database session
    Returns:
        List of genres
    """
    genres = crud.get_all_categories(db)
    genre_strings: list[str] = [genre.name for genre in genres]  # type: ignore

    try:
        return schemas.GenresList(genres=genre_strings)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving genres: {str(e)}"
        )
