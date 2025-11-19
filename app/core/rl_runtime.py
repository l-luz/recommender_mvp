"""
SINGLETON runtime for the RL Recommendation System.
"""

from app.core.recommender.linucb import LinUCBRecommender
from app.core.training import OnlineTrainer
from app.core.context_features import ContextFeatures
from  app.db import crud, database

# ------------------------------------------------------------
# Load catalog and create mapping book_id -> arm index
# ------------------------------------------------------------
BOOK_IDS = crud.get_all_book_ids(next(database.get_db()))
ARM_INDEX = {bid: i for i, bid in enumerate(BOOK_IDS)}

N_ARMS = len(BOOK_IDS)
FEATURE_DIM = 6  # TODO: test dimensions

# ------------------------------------------------------------
# Global instance of the RL model
# ------------------------------------------------------------

recommender = LinUCBRecommender(
    n_arms=N_ARMS,
    d=FEATURE_DIM,
    alpha=1.0
)

trainer = OnlineTrainer(
    recommender=recommender,
    batch_size=32
)

features = ContextFeatures()

__all__ = ["recommender", "trainer", "features", "ARM_INDEX", "BOOK_IDS"]
