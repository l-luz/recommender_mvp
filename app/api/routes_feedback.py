"""
Rota /feedback -> registra like/dislike de usuários
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud, models, database
from app.db.models import ActionType
from app.api import schemas
from app.core import rl_runtime as rl
from app.core.context_features import ContextFeatures


router = APIRouter(prefix="/feedback", tags=["feedback"])

#
# ==================== Auxiliary Functions ====================
#


def _feedback_type_to_action_type(action_type: schemas.ActionType) -> ActionType:
    """Converts ActionType (API) to ActionType (DB)"""
    mapping = {
        schemas.ActionType.LIKE: ActionType.LIKE,
        schemas.ActionType.DISLIKE: ActionType.DISLIKE,
        schemas.ActionType.CLEAR: ActionType.CLEAR,
    }
    return mapping[action_type]


def _calculate_reward(action_type: schemas.ActionType) -> float:
    """Calculate reward based on feedback type"""
    rewards = {
        schemas.ActionType.LIKE: 1.0,
        schemas.ActionType.CLEAR: 0.5,
        schemas.ActionType.DISLIKE: -1,
    }
    return rewards[action_type]


#
# ==================== Endpoints ====================
#


@router.post("/register", response_model=schemas.FeedbackResponse)
def register_feedback(
    feedback: schemas.FeedbackRequest, db: Session = Depends(database.get_db)
) -> schemas.FeedbackResponse:
    """    
    Registers user feedback about a book.    
    Args:    
        feedback: FeedbackRequest with user_id, book_id, action_type, slate_id, pos    
    db: Database session    
    Returns:    
        FeedbackResponse confirming registration    
    Raises:    
        HTTPException: If user or book does not exist    
        db: Database session
    """


    user = crud.get_user(db, feedback.user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {feedback.user_id} not found"
        )

    book = crud.get_book(db, feedback.book_id)
    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book {feedback.book_id} not found"
        )

    # Convert feedback type
    action_type = _feedback_type_to_action_type(feedback.action_type)

    last_event = crud.get_user_last_book_event(db, feedback.user_id, feedback.book_id)
    # Calculate reward based on action type
    reward = _calculate_reward(feedback.action_type)
   
    slate_id = feedback.slate_id or ""
    pos = feedback.pos or -1

    ctx = ContextFeatures().get_context(
        user_id=feedback.user_id, book_id=feedback.book_id, db=db
    )

    arm_index = rl.ARM_INDEX[feedback.book_id]

    try:
        event = crud.create_event(
            db=db,
            user_id=feedback.user_id,
            book_id=feedback.book_id,
            slate_id=slate_id,
            pos=pos, 
            action_type=action_type.value,  # Convert Enum to string
            reward_w=reward,  # weight-adjusted reward
            ctx_features=feedback.ctx_features,
        )
        if rl.trainer is None:
            raise RuntimeError("RL trainer not initialized")
        rl.trainer.add_feedback(ctx, arm_index, reward)
            
        return schemas.FeedbackResponse(
            success=True,
            message=f"Feedback '{feedback.action_type.value}' registered successfully",
            event_id=event.id,  # type: ignore
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error registering feedback: {str(e)}"
        )


@router.get("/user/{user_id}/likes", response_model=schemas.BookList)
def get_user_likes(user_id: int, db: Session = Depends(database.get_db)) -> dict:
    """
    Returns all books that a user has liked.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        Dict with list of books
    """

    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    books = crud.get_user_liked_books_current(db, user_id)

    return {
        "user_id": user_id,
        "total": len(books),
        "books": [
            {
                "id": book.id,
                "title": book.title,
                "authors": ','.join(book.get_authors_list) if book.get_authors_list else "N/A", # type: ignore
                "genre": ','.join(book.get_categories_list) if book.get_categories_list else "N/A",  # type: ignore
                "avg_rating": book.avg_rating,
                "image": book.get_image or "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
            }
            for book in books
        ],
    }


@router.get("/user/{user_id}/dislikes", response_model=schemas.BookList)
def get_user_dislikes(user_id: int, db: Session = Depends(database.get_db)) -> dict:
    """
    Returns all books that a user has disliked.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        Dict with list of books
    """

    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    books = crud.get_user_disliked_books_current(db, user_id)

    return {
        "user_id": user_id,
        "total": len(books),
        "books": [
            {
                "id": book.id,
                "title": book.title,
                "authors": ','.join(book.get_authors_list) if book.get_authors_list else "N/A", # type: ignore
                "genre": ','.join(book.get_categories_list) if book.get_categories_list else "N/A",  # type: ignore
                "avg_rating": book.avg_rating,
                "image": book.get_image or "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
            }
            for book in books
        ],
    }


@router.get("/user/{user_id}/history", response_model=schemas.HistorySummary)
def get_user_history(user_id: int, db: Session = Depends(database.get_db)) -> dict:
    """
    Returns complete history of a user's interactions.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        Dict with complete statistics
    """

    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    all_events = crud.get_user_events(db, user_id)

    likes_count = 0
    dislikes_count = 0

    for event in all_events:
        if str(event.action_type) == "ActionType.LIKE" or str(event.action_type) == "like":  # type: ignore
            likes_count += 1
        elif str(event.action_type) == "ActionType.DISLIKE" or str(event.action_type) == "dislike":  # type: ignore
            dislikes_count += 1

    return {
        "user_id": user_id,
        "total_events": len(all_events),
        "likes": likes_count,
        "dislikes": dislikes_count,
        "unique_books_interacted": len(set(e.book_id for e in all_events)),  # type: ignore
    }
