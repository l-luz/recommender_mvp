"""
Base interface for all recommenders (hotspot).
"""

from typing import List
import numpy as np


class BaseRecommender:
    """
    Interface for reinforcement learning recommendation algorithms.
    """

    def recommend(
        self, candidate_arms: List[int], contexts: np.ndarray, n_recommendations: int
    ) -> List[int]:
        """
        Returns a list of selected arms.

        Args:
            context: Vector of context features (shape: context_dim,)
            n_recommendations: Number of recommendations

        Returns:
            List of indexes of recommended items
        """
        raise NotImplementedError

    def update(self, context: np.ndarray, arm: int, reward: float):
        """
        Update the model in a single step (online learning).

        Args:
        context: Context vector
        arm: Index of the item that received feedback
        reward: Reward (0 or 1 for like/dislike)
        """
        raise NotImplementedError

    def batch_update(self, contexts: np.ndarray, arms: np.ndarray, rewards: np.ndarray):
        """
        Updates in mini-batches — by default, it just calls update repeatedly.

        Args:
        contexts: Array of contexts (shape: n_samples, context_dim)
                    arms: Array of selected items (shape: n_samples,)
                    rewards: Array of rewards (shape: n_samples,)
        """
        for x, a, r in zip(contexts, arms, rewards):
            self.update(x, int(a), float(r))

    def _to_dict(self) -> dict:
        """
        Serializes the internal state into a pure dictionary.
        """
        raise NotImplementedError

    def _from_dict(self, data: dict) -> None:
        """
        Creates an instance from a serialized dictionary.
        """
        raise NotImplementedError

    def save_state(self, path: str):
        raise NotImplementedError

    def load_state(self, path: str, valid_arms: list[int], d_expected: int) -> None:
        """
        Loads the state of a file, reconciling it with the current branches.
        """
        raise NotImplementedError
