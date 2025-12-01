"""
Online model update (mini-batchs)
"""

from typing import List, Tuple
import numpy as np

from app.utils.config import RECOMMENDER_CONFIG
from .context_features import ContextFeatures


class OnlineTrainer:
    """
    Manages online model updates with mini-batches.
    """

    def __init__(self, recommender, batch_size: int = 32):
        """
        Initialize trainer.

        Args:
            recommender: ContextualRecommender instance
            batch_size: Mini-batch size for update
        """
        self.recommender = recommender
        self.batch_size = batch_size
        self.buffer: List[Tuple] = []  # buffer (context, arm, reward)

    def add_feedback(self, context: np.ndarray, arm: int, reward: float):
        """
        Adds feedback to the buffer.

        Args:
            context: Context vector
            arm: Selected item
            reward: Reward
        """
        self.buffer.append((context, arm, reward))

        if len(self.buffer) >= self.batch_size:
            self.flush()

    def flush(self):
        """
        Processes accumulated buffer and updates template.
        """
        if not self.buffer:
            return

        contexts = np.array([x[0] for x in self.buffer])
        arms = np.array([x[1] for x in self.buffer])
        rewards = np.array([x[2] for x in self.buffer])

        self.recommender.batch_update(contexts, arms, rewards)
        self.buffer.clear()

        model_path = RECOMMENDER_CONFIG["model_path"]
        if model_path and hasattr(self.recommender, "save_state"):
            try:
                self.recommender.save_state(model_path)
            except Exception as e:
                print(f"[WARN] Falha ao salvar estado LinUCB: {e}")
