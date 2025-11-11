"""
Lógica do Bandit Contextual (mabwiser/contextualbandits)
"""

from typing import List, Dict, Tuple
import numpy as np


class ContextualRecommender:
    """
    Recommender usando MABWiser (LinUCB/LinTS) para aprendizado contextual.
    """
    
    def __init__(self, n_arms: int, context_dim: int, model_type: str = "linucb"):
        """
        Inicializa o recommender.
        
        Args:
            n_arms: Número de itens (livros) a considerar
            context_dim: Dimensionalidade das features de contexto
            model_type: Tipo de modelo ("linucb" ou "lints")
        """
        self.n_arms = n_arms
        self.context_dim = context_dim
        self.model_type = model_type
        # TODO: Inicializar mabwiser.UCB ou mabwiser.LinUCB
        pass
    
    def recommend(
        self,
        context: np.ndarray,
        n_recommendations: int = 4
    ) -> List[int]:
        """
        Retorna recomendações baseadas em contexto.
        
        Args:
            context: Vetor de features de contexto (shape: context_dim,)
            n_recommendations: Número de recomendações
        
        Returns:
            Lista de índices de itens recomendados
        """
        # TODO: Usar modelo.predict() ou similar
        pass
    
    def update(self, context: np.ndarray, arm: int, reward: float):
        """
        Atualiza o modelo com novo feedback.
        
        Args:
            context: Vetor de contexto
            arm: Índice do item que recebeu feedback
            reward: Recompensa (0 ou 1 para like/dislike)
        """
        # TODO: Chamar modelo.partial_fit() ou .fit()
        pass
    
    def batch_update(
        self,
        contexts: np.ndarray,
        arms: np.ndarray,
        rewards: np.ndarray
    ):
        """
        Atualização em mini-batch para melhor eficiência.
        
        Args:
            contexts: Array de contextos (shape: n_samples, context_dim)
            arms: Array de items selecionados (shape: n_samples,)
            rewards: Array de recompensas (shape: n_samples,)
        """
        # TODO: Atualizar modelo com múltiplos samples
        pass
