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
# Endpoints
#


@router.post("/recommend", response_model=schemas.SlateResponse)
def get_recommendations(
    request: schemas.SlateRequest, db: Session = Depends(database.get_db)
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

