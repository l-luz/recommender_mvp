"""
Generation of context features (user + item)
"""

from typing import List, Optional
import numpy as np
from sqlalchemy.orm import Session

from app.db import crud, models
from app.api import schemas
import math

class ContextFeatures:
    """
    Extracts and combines user and item features for context.
    """

    def __init__(self, feature_dim: int = 8):
        """
        Initializes feature extractor.

        Args:
        feature_dim: Dimensionality of the context vector
        """
        self.user_dim = 3
        self.item_dim = 3
        self.feature_dim = self.user_dim + self.item_dim

    def get_user_features(
        self,
        user_id: int,
        db: Optional[Session] = None,
    ) -> np.ndarray:
        """
        Extract user features (preferred genres, history, etc.).

        Args:
            user_id: User ID
            db: DB session for queries

        Returns:
            Vector of features (shape: feature_dim,)
            Test: [ like_rate, activity, bias, engagement_rate ]
                - 
                - like_rate: likes / (likes + dislikes)
                - activity: min(total_events / 50, 1.0)
                - bias: 1.0 (constante)
        """
        if db is None:
            return np.array([0.5, 0.0, 1.0], dtype=float)

        like_events = crud.get_user_events(db, user_id, schemas.ActionType.LIKE)
        dislike_events = crud.get_user_events(db, user_id, schemas.ActionType.DISLIKE)

        # cleared_events = crud.get_user_events(db, user_id, schemas.ActionType.CLEAR) # the clear function will be trouble ...

        all_events = crud.get_user_events(db, user_id)
        total_events = len(all_events)
    
        if total_events == 0:
            like_rate = 0.5
            activity = 0.0
            engagement = 0
        else:
            likes = len(like_events)
            dislikes = len(dislike_events)
            engagement = likes + dislikes

            if engagement == 0:
                like_rate = 0.5
            else:
                like_rate = likes / engagement
                

            activity = min(total_events / 50.0, 1.0)

        bias = 1.0

        return np.array([like_rate, activity, bias], dtype=float)

    def get_item_features(
        self,
        book_id: int,
        db: Optional[Session] = None,
        user_preferred_genres: Optional[List[str]] = None,
    ) -> np.ndarray:

        """
        Extraia características do livro (gênero, incorporações, etc.).

        Argumentos:
        book_id: ID do livro
        db: Sessão do banco de dados

        Retorna:
        Vetor de características (forma: feature_dim,)
        Teste: 3 [ norm_rating, norm_popularity, genre_match ]
                    - norm_rating: (avg_rating ou 0) / 5.0
        - norm_popularity: normalização de log(1 + ratings_count)
        - genre_match: se intersecta com gêneros favoritos do usuário
        """
        if db is None:
            return np.array([0.0, 0.0, 0.5], dtype=float)

        book: Optional[models.Book] = crud.get_book(db, book_id)
        if not book:
            return np.array([0.0, 0.0, 0.5], dtype=float)

        # normalized average rating
        avg_rating = book.avg_rating if book.avg_rating is not None else 0.0
        norm_rating = max(min(avg_rating / 5.0, 1.0), 0.0)

        # normalized popularity
        ratings_count = book.ratings_count or 0

        REF_MAX = 1000
        norm_popularity = math.log1p(ratings_count) / math.log1p(REF_MAX) # type: ignore
        norm_popularity = max(min(norm_popularity, 1.0), 0.0)

        # gender match with user preferences
        genre_match = 0.5
        if user_preferred_genres is not None:
            book_cats = book.get_categories_list
            prefs = [g.lower().strip() for g in user_preferred_genres] # TODO: Check db cleaning
            if not prefs:
                genre_match = 0.5
            else:
                has_intersection = any(c in prefs for c in book_cats)
                genre_match = 1.0 if has_intersection else 0.0

        return np.array([norm_rating, norm_popularity, genre_match], dtype=float)

    def _combine_features(
        self,
        user_feat: np.ndarray,
        item_feat: np.ndarray,
    ) -> np.ndarray:
        """
        Combines user and item features.

        Args:
            user_feat: User features
            item_feat: Item features

        Returns:
            Combined context vector
        """
        vec = np.concatenate([user_feat, item_feat]).astype(float)
        if vec.shape[0] < self.feature_dim:
            pad = np.zeros(self.feature_dim - vec.shape[0], dtype=float)
            vec = np.concatenate([vec, pad])
        elif vec.shape[0] > self.feature_dim:
            # cut if it is larger than planned
            vec = vec[: self.feature_dim]
        return vec

    def get_context(        self,
        user_id: int,
        book_id: int,
        db: Optional[Session] = None,
        user_preferred_genres: Optional[List[str]] = None,
) -> np.ndarray:
        """
        Wrapper: returns complete user + item context.

        Args:
        user_id: User ID
        book_id: Book ID
        db: DB session

        Returns:
        Context vector
        """
        user_feat = self.get_user_features(user_id, db=db)
        item_feat = self.get_item_features(
            book_id,
            db=db,
            user_preferred_genres=user_preferred_genres,
        )
        return self._combine_features(user_feat, item_feat)
