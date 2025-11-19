"""
Route /slate -> returns book recommendations
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.rl_runtime import recommender, features, ARM_INDEX
import numpy as np
from app.db import crud, database
from app.api import schemas
import random
import uuid

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
        slate_id = str(uuid.uuid4())


        # recommended_books= _random_approach(db, user_id, n_items)
        recommended_books_ids = _rl_approach(db, user_id, n_items)
        recommended_data = []
        for b_idx in recommended_books_ids:
            book = crud.get_book(db, b_idx)
            if book:
                data = {
                    "book_id": b_idx,
                    "title": book.title,
                    "description": book.description or "No description available.",
                    "score": book.avg_rating,
                    "image": book.get_image or "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
                    }
                data["authors"] =  ','.join(book.get_authors_list) if book.get_authors_list else "N/A" # type: ignore
                data["genre"] = ','.join(book.get_categories_list) if book.get_categories_list else "N/A"  # type: ignore
                recommended_data.append(data)

        return {
            "user_id": user_id,
            "slate_id": slate_id,
            "total": n_items,
            "recommendations": recommended_data,
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Error generating recommendations: {str(e)}"
        )

def _random_approach(db, user_id, n_items):
    all_books = crud.get_all_books(db, skip=0, limit=100)

    random_books = random.sample(all_books, min(n_items, len(all_books)))
                    
    return random_books

def _rl_approach(db, user_id, n_items):
    all_books = crud.get_all_books(db)

    candidate_books = random.sample(all_books, k=min(len(all_books), 30))

    contexts = []
    arms = []

    for book in candidate_books:
        ctx = features.get_context(user_id, book.id, db=db) # type: ignore
        contexts.append(ctx)
        arms.append(book.id)

    contexts = np.array(contexts)

    chosen_books_ids = recommender.recommend(
        candidate_arms=arms,
        contexts=contexts,
        n_recommendations=n_items
    )
    return chosen_books_ids

