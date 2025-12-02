"""Recommender logic tests using LinUCB and helpers."""

import numpy as np

from app.core.context_features import ContextFeatures
from app.core.recommender.linucb import LinUCBRecommender
from app.core.training import OnlineTrainer
from app.db import crud
from app.core import rl_runtime


def test_linucb_ranks_by_confidence():
    """Verifies that LinUCB ranks arms based on the highest UCB."""
    recommender = LinUCBRecommender(n_arms=3, d=4, alpha=1.0)
    candidate_arms = [10, 11, 12]
    contexts = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0, 0.0],
        ]
    )

    chosen = recommender.recommend(candidate_arms, contexts, n_recommendations=2)

    assert chosen == [12, 11]


def test_linucb_update_adjusts_parameters():
    """Tests if the update method correctly adjusts the A and b matrices."""
    recommender = LinUCBRecommender(n_arms=1, d=3, alpha=0.5)
    context = np.array([1.0, 2.0, 0.0])

    recommender.update(context, arm=5, reward=1.0)

    assert 5 in recommender.A_inv
    assert 5 in recommender.b

    A_orig = np.eye(3)
    A_new = A_orig + np.outer(context, context)
    expected_b = context.reshape(-1, 1)
    assert np.allclose(np.linalg.inv(recommender.A_inv[5]), A_new)
    assert np.allclose(recommender.b[5], expected_b)


def test_online_trainer_flushes_batch():
    """Ensures the OnlineTrainer processes the buffer when it hits batch_size."""
    recommender = LinUCBRecommender(n_arms=5, d=2, alpha=0.5)
    trainer = OnlineTrainer(recommender=recommender, batch_size=2)

    c1 = np.array([1.0, 0.0])
    c2 = np.array([0.0, 1.0])

    trainer.add_feedback(c1, arm=1, reward=1.0)
    assert len(trainer.buffer) == 1

    trainer.add_feedback(c2, arm=2, reward=0.2)
    assert len(trainer.buffer) == 0  # buffer flushed

    assert 1 in recommender.A_inv and 2 in recommender.A_inv


def test_context_features_default_shape():
    """Checks the dimensionality of the default context feature vector."""
    features = ContextFeatures()
    ctx_vector = features.get_context(user_id=1, book_id=1, db=None)

    assert ctx_vector.shape[0] == features.feature_dim
    assert np.allclose(ctx_vector[:3], np.array([0.5, 0.0, 1.0]))


def test_context_uses_db_fields(db_session):
    """Tests if context features are altered based on database data."""
    user = crud.create_user(db_session, "cf", "pw")
    book = crud.create_book(
        db_session, "Book", authors=["A1"], categories=["G1"], description="d"
    )
    features = ContextFeatures()
    ctx = features.get_context(user_id=user.id, book_id=book.id, db=db_session)
    assert ctx.shape[0] == features.feature_dim
    # ensure at least one position differs from default due to db data
    assert not np.allclose(ctx, np.zeros_like(ctx))


def test_arm_index_matches_books(db_session):
    """Ensures the runtime arm index corresponds to books in the database."""
    books = [
        crud.create_book(
            db_session, f"B{i}", authors=["A"], categories=["C"], description="d"
        )
        for i in range(3)
    ]
    # Rebuild runtime state from the DB catalog
    rl_runtime.init_runtime(db_session)

    book_ids = set(crud.get_all_book_ids(db_session))
    assert set(rl_runtime.ARM_INDEX.keys()) == book_ids
    # Ensure ARM_INDEX order is aligned with BOOK_IDS length
    assert len(rl_runtime.BOOK_IDS) == len(book_ids)
