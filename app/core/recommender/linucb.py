"""
Contextual Bandit Logic (LinUCB)
"""

import numpy as np
from .base import BaseRecommender
from typing import Dict, List


class LinUCBRecommender(BaseRecommender):
    """
    Implements the LinUCB (Linear Upper Confidence Bound) algorithm for disjoint linear models.

    This recommender maintains separate ridge regression estimates for each arm
    to calculate an upper confidence bound for the expected reward.
    """

    def __init__(self, n_arms: int, d: int, alpha: float = 1.0):
        """
        Initializes the LinUCB recommender with identity matrices.

        Args:
            n_arms: Number of distinct arms (items) available in the pool.
            d: Dimension of the context feature vector.
            alpha: Exploration parameter. Higher values increase the confidence bound width,
                   encouraging more exploration of uncertain arms.
        """
        self.d = d  # dimension
        self.alpha = alpha  # exploration factor
        
        # Key: BookID (int), Value: Matrix/Vector
        self.A_inv: Dict[int, np.ndarray] = {}  # Inverse of context covariance
        self.b: Dict[int, np.ndarray] = {}  # context-reward relationship

    def _init_arm(self, arm_id: int):
        """
        Lazy initialization: if we haven't seen this book ID before,
        create its A_inv and b matrices.
        """
        if arm_id not in self.A_inv:
            # Initialize A_inv as Identity (since A=I, A^-1=I)
            self.A_inv[arm_id] = np.eye(self.d)
            self.b[arm_id] = np.zeros((self.d, 1))

    def recommend(
        self, candidate_arms: List[int], contexts: np.ndarray, n_recommendations: int
    ) -> List[int]:
        """
        Selects the top-k arms based on their Upper Confidence Bound scores.

        Args:
            candidate_arms: List of arm indices that are eligible for recommendation.
            contexts: A numpy array of context vectors corresponding to the candidate_arms.
                      Expected shape: (len(candidate_arms), d).
            n_recommendations: The maximum number of items to return.

        Returns:
            A list of selected arm indices, sorted by their estimated UCB score (descending).
        """
        scores = []

        for arm, x in zip(candidate_arms, contexts):
            self._init_arm(arm)
            x = x.reshape(-1, 1)

            A_inv = self.A_inv[arm]

            theta = A_inv @ self.b[arm]  # Coefficient estimates

            # UCB Score Calculation
            mean = theta.T @ x  # Mean prediction (exploitation)
            
            # Variance calculation (exploration term)
            var = np.sqrt(x.T @ A_inv @ x)
            
            p = (mean + self.alpha * var).item()
            scores.append(p)

        scores = np.array(scores)
        ranked_indices = scores.argsort()[::-1]

        # Map back to Book IDs
        K = min(n_recommendations, len(candidate_arms))
        chosen_arms = [candidate_arms[i] for i in ranked_indices[:K]]

        return chosen_arms

    def update(self, context, arm, reward):
        """
        Updates the model parameters for a specific arm using the observed feedback.

        This performs an online update of the inverse covariance matrix A_inv 
        using the Sherman-Morrison formula and updates vector b.

        Args:
            context: The context vector associated with the chosen arm (shape: [d]).
            arm: The index of the arm that was executed.
            reward: The reward value observing from the environment.
        """
        self._init_arm(arm)
        x = context.reshape(-1, 1)
        
        self.b[arm] += reward * x
        
        A_inv_old = self.A_inv[arm]
        
        numerator = (A_inv_old @ x) @ (x.T @ A_inv_old)
        
        denominator = 1.0 + (x.T @ A_inv_old @ x).item()
        
        self.A_inv[arm] = A_inv_old - (numerator / denominator)