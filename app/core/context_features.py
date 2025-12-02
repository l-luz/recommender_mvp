"""
Generation of context features (user + item)
"""

from typing import List, Optional
import numpy as np
from sqlalchemy.orm import Session
from app.utils.config import RECOMMENDER_CONFIG
from app.db import crud, models
from app.api import schemas
import math
import json
import os


def _load_item_config(path: str = RECOMMENDER_CONFIG["item_config"]):
    """
    Load item configuration (top categories/authors/publishers) generated
    offline by the build_item_features notebook.

    Expected JSON format:
    {
      "top_categories_ids": List(int),
      "top_authors_ids": List(int),
      "top_publishers": List(str)
    """
    if not os.path.exists(path):
        print(f"[WARN] Arquivo de configuração de itens não encontrado em '{path}'. Usando listas vazias.")
        return {
            "top_categories_ids": [],
            "top_authors_ids": [],
            "top_publishers": [],
        }

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalizes keys and types
    cat_ids = data.get("top_categories", [])
    author_ids = data.get("top_authors", [])
    publishers = data.get("top_publishers", [])

    # Ensures correct types
    cat_ids = [int(x) for x in cat_ids]
    author_ids = [int(x) for x in author_ids]
    publishers = [(p or "").lower().strip() for p in publishers if p]

    return {
        "top_categories_ids": cat_ids,
        "top_authors_ids": author_ids,
        "top_publishers": publishers,
    }


class ContextFeatures:
    """
    Extracts and combines user and item features for context.
    """

    def __init__(self):
        """
        Initializes feature extractor.

        Dimensions:

        user_features: 3
            [ like_rate, activity, bias ]

        item_features:
            [ norm_rating, norm_popularity, genre_match,
              multi-hot categories, multi-hot authors, multi-hot publishers ]
        """

        self.user_dim = 3  # like_rate, activity, bias

        cfg = _load_item_config()

        self.top_category_ids: List[int] = cfg["top_categories_ids"]
        self.top_author_ids: List[int] = cfg["top_authors_ids"]
        self.top_publishers: List[str] = cfg["top_publishers"]

        # maps id -> index (for multi-hot)
        self.cat_index = {cid: i for i, cid in enumerate(self.top_category_ids)}
        self.author_index = {aid: i for i, aid in enumerate(self.top_author_ids)}
        self.publisher_index = {name: i for i, name in enumerate(self.top_publishers)}

        # 3 numerical (rating, popularity, genre_match) +
        # K_cats + K_authors + K_publishers
        self.item_dim = (
            3
            + len(self.top_category_ids)
            + len(self.top_author_ids)
            + len(self.top_publishers)
        )

        # total context size
        self.feature_dim = self.user_dim + self.item_dim

    def get_user_features(
        self,
        user_id: int,
        db: Optional[Session] = None,
    ) -> np.ndarray:
        """
        Extract user features.

        Returns:
            [ like_rate, activity, bias ]

            - like_rate: likes / (likes + dislikes), default 0.5 se sem engajamento
            - activity: min(total_events / 50, 1.0)
            - bias: 1.0 (constante)
        """
        if db is None:
            return np.array([0.5, 0.0, 1.0], dtype=float)

        like_events = crud.get_user_events(db, user_id, schemas.ActionType.LIKE)
        dislike_events = crud.get_user_events(db, user_id, schemas.ActionType.DISLIKE)
        all_events = crud.get_user_events(db, user_id)

        total_events = len(all_events)

        if total_events == 0:
            like_rate = 0.5
            activity = 0.0
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
        Extracts characteristics from the book.

        Returns vector:
        [ norm_rating, norm_popularity, genre_match,
        multi-hot categories, multi-hot authors, multi-hot publishers ]

        - norm_rating: (avg_rating or 0) / 5.0
                - norm_popularity: normalization of log(1 + ratings_count)
        - genre_match: 1.0 if the book shares any genre with user preferences,
                            0.0 if not, 0.5 if preferences are empty/null
        - categories/authors/publishers: multi-hot based on JSON top_* lists
        """
        if db is None:
            return np.zeros(self.item_dim, dtype=float)

        book: Optional[models.Book] = crud.get_book(db, book_id)
        if not book:
            return np.zeros(self.item_dim, dtype=float)

        # numerical features: rating and popularity
        avg_rating = book.avg_rating if book.avg_rating is not None else 0.0
        norm_rating = max(min(avg_rating / 5.0, 1.0), 0.0)

        ratings_count = book.ratings_count or 0
        REF_MAX = 1000
        norm_popularity = math.log1p(ratings_count) / math.log1p(REF_MAX)  # type: ignore
        norm_popularity = max(min(norm_popularity, 1.0), 0.0)

        # genre_match with user preferences
        genre_match = 0.5
        if user_preferred_genres is not None:
            book_cats = [g.lower().strip() for g in book.get_categories_list]
            prefs = [g.lower().strip() for g in user_preferred_genres]
            if prefs:
                has_intersection = any(c in prefs for c in book_cats)
                genre_match = 1.0 if has_intersection else 0.0

        num_feats = np.array([norm_rating, norm_popularity, genre_match], dtype=float)

        # multi-hot categories (by ID)
        cat_vec = np.zeros(len(self.top_category_ids), dtype=float)
        if self.top_category_ids:
            for c in book.categories_rel:
                cid = int(c.id)
                if cid in self.cat_index:
                    idx = self.cat_index[cid]
                    cat_vec[idx] = 1.0

        # multi-hot authors (by ID)
        author_vec = np.zeros(len(self.top_author_ids), dtype=float)
        if self.top_author_ids:
            for a in book.authors_rel:
                aid = int(a.id)
                if aid in self.author_index:
                    idx = self.author_index[aid]
                    author_vec[idx] = 1.0

        # multi-hot publishers (by normalized string)
        pub_vec = np.zeros(len(self.top_publishers), dtype=float)
        if self.top_publishers:
            pub_name = (book.publisher or "").lower().strip()
            if pub_name in self.publisher_index:
                idx = self.publisher_index[pub_name]
                pub_vec[idx] = 1.0

        item_vec = np.concatenate([num_feats, cat_vec, author_vec, pub_vec])

        # sanity check
        if item_vec.shape[0] != self.item_dim:
            raise ValueError(
                f"item_vec com tamanho {item_vec.shape[0]}, esperado {self.item_dim}"
            )

        return item_vec

    def _combine_features(
        self,
        user_feat: np.ndarray,
        item_feat: np.ndarray,
    ) -> np.ndarray:
        """
        Combines user and item features.

        Returns:
            Combined context vector
        """
        vec = np.concatenate([user_feat, item_feat]).astype(float)
        if vec.shape[0] < self.feature_dim:
            pad = np.zeros(self.feature_dim - vec.shape[0], dtype=float)
            vec = np.concatenate([vec, pad])
        elif vec.shape[0] > self.feature_dim:
            vec = vec[: self.feature_dim]
        return vec

    def get_context(
        self,
        user_id: int,
        book_id: int,
        db: Optional[Session] = None,
        user_preferred_genres: Optional[List[str]] = None,
    ) -> np.ndarray:
        """
        Wrapper: returns complete user + item context.

        Returns:
            Context vector of size feature_dim
        """
        user_feat = self.get_user_features(user_id, db=db)
        item_feat = self.get_item_features(
            book_id,
            db=db,
            user_preferred_genres=user_preferred_genres,
        )
        return self._combine_features(user_feat, item_feat)
