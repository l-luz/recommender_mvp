"""
Route /slate -> returns book recommendations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.db import crud, database
from app.api import schemas


#
# Router Setup
#

router = APIRouter(prefix="/slate", tags=["slate"])


#
# Schemas
#


class SlateRequest(BaseModel):
    """Request form for getting recommendations"""

    user_id: int
    n_items: int = 4


class BookRecommendation(BaseModel):
    """Return model for book recommendation"""

    book_id: int
    title: str
    authors: str
    avg_rating: float


class SlateResponse(BaseModel):
    """Response form for recommendations"""

    user_id: int
    slate_id: str
    total: int
    books: List[BookRecommendation]


#
# Endpoints
#


@router.post("/recommend", response_model=SlateResponse)
def get_recommendations(
    request: SlateRequest, db: Session = Depends(database.get_db)
) -> dict:
    """
    Returns a slate (list) of recommendations for a user.

    Args:
        request: SlateRequest with user_id and n_items
        db: Database session

    Returns:
        SlateResponse with list of recommendations

    Raises:
        HTTPException: If user does not exist
    """
    user = crud.get_user(db, request.user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {request.user_id} not found"
        )

    try:
        # Get all available books
        all_books = crud.get_all_books(db, skip=0, limit=100)

        # Simple recommendation: return random books (TODO: integrate MABWiser)
        import random
        import uuid

        recommended_books = random.sample(all_books, min(request.n_items, len(all_books)))

        slate_id = str(uuid.uuid4())

        return {
            "user_id": request.user_id,
            "slate_id": slate_id,
            "total": len(recommended_books),
            "books": [
                {
                    "book_id": book.id,
                    "title": book.title,
                    "authors": book.authors or "Unknown",
                    "avg_rating": book.avg_rating or 0.0,
                }
                for book in recommended_books
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating recommendations: {str(e)}"
        )
