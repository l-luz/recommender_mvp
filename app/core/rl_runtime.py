"""
SINGLETON runtime for the RL Recommendation System.
"""

from app.core.recommender.linucb import LinUCBRecommender
from app.core.training import OnlineTrainer
from app.core.context_features import ContextFeatures
from app.utils.config import RECOMMENDER_CONFIG
from sqlalchemy.orm import Session
from app.db import crud

recommender: LinUCBRecommender | None = None
trainer: OnlineTrainer | None = None
features: ContextFeatures | None = None
ARM_INDEX: dict[int, int] = {}
BOOK_IDS: list[int] = []


def init_runtime(db: Session):
    """
    Initializes the recommendation system. Should only be called once.
    """
    global recommender, trainer, features, ARM_INDEX, BOOK_IDS

    BOOK_IDS.clear()
    BOOK_IDS.extend(crud.get_all_book_ids(db))

    ARM_INDEX.clear()
    ARM_INDEX.update({bid: i for i, bid in enumerate(BOOK_IDS)})

    n_arms = len(BOOK_IDS)
    RECOMMENDER_CONFIG["n_arms"] = n_arms

    features = ContextFeatures()
    RECOMMENDER_CONFIG["feature_dim"] = features.feature_dim

    recommender = LinUCBRecommender(
        n_arms=n_arms,
        d=RECOMMENDER_CONFIG["feature_dim"],
        alpha=RECOMMENDER_CONFIG["alpha"],
    )

    model_path = RECOMMENDER_CONFIG.get("model_path")
    if model_path:
        try:
            recommender.load_state(
                path=model_path,
                valid_arms=BOOK_IDS,
                d_expected=features.feature_dim,
            )
        except Exception as e:
            print(f"[WARN] Falha ao carregar estado LinUCB: {e}")

    trainer = OnlineTrainer(
        recommender=recommender, batch_size=RECOMMENDER_CONFIG["batch_size"]
    )

__all__ = [
    "recommender",
    "trainer",
    "features",
    "ARM_INDEX",
    "BOOK_IDS",
    "init_runtime",
]
