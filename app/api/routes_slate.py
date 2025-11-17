"""
Route /slate -> returns book recommendations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
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
    user_id: int,
    n_items: int, db: Session = Depends(database.get_db)
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
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {user_id} not found"
        )

    try:
        # Get all available books
        all_books = crud.get_all_books(db, skip=0, limit=100)

        # Simple recommendation: return random books (TODO: integrate MABWiser)
        import random
        import uuid
        slate_id = str(uuid.uuid4())

        recommended_books = random.sample(all_books, min(n_items, len(all_books)))
        recommended_data = []
        for book in recommended_books:
            data = {
                "book_id": book.id,
                "title": book.title,
                "description": book.description or "No description available.",
                "score": book.avg_rating,
                "image": book.get_image or "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
                }
            data["authors"] =  ','.join(book.get_list_fiel("authors")) if book.get_list_fiel("authors") else "N/A" # type: ignore
            data["genre"] = ','.join(book.get_list_fiel("categories_raw")) if book.get_list_fiel("categories_raw") else "N/A"  # type: ignore
            recommended_data.append(data)
                        
        return {
            "user_id": user_id,
            "slate_id": slate_id,
            "total": len(recommended_books),
            "recommendations": recommended_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating recommendations: {str(e)}"
        )

