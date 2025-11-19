"""
SINGLETON runtime for the RL Recommendation System.
"""

from app.core.recommender.linucb import LinUCBRecommender
from app.core.training import OnlineTrainer
from app.core.context_features import ContextFeatures
from  app.db import crud, database
from app.utils.config import RECOMMENDER_CONFIG

# ------------------------------------------------------------
# Load catalog and create mapping book_id -> arm index
# ------------------------------------------------------------
BOOK_IDS = crud.get_all_book_ids(next(database.get_db()))
ARM_INDEX = {bid: i for i, bid in enumerate(BOOK_IDS)}

n_arms = len(BOOK_IDS)
RECOMMENDER_CONFIG["n_arms"] = n_arms

# ------------------------------------------------------------
# Global instance of the RL model
# ------------------------------------------------------------


features = ContextFeatures()
RECOMMENDER_CONFIG["feature_dim"] = features.feature_dim

recommender = LinUCBRecommender(
    n_arms=n_arms,
    d=RECOMMENDER_CONFIG["feature_dim"],
    alpha=RECOMMENDER_CONFIG["alpha"]
)

trainer = OnlineTrainer(
    recommender=recommender,
    batch_size=RECOMMENDER_CONFIG["batch_size"]
)


__all__ = ["recommender", "trainer", "features", "ARM_INDEX", "BOOK_IDS"]
