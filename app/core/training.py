"""
Atualização online do modelo (mini-batch)
"""

from typing import List, Tuple
import numpy as np
from .context_features import ContextFeatures


class OnlineTrainer:
    """
    Gerencia atualização online do modelo com mini-batches.
    """
    
    def __init__(self, recommender, batch_size: int = 32):
        """
        Inicializa trainer.
        
        Args:
            recommender: Instância de ContextualRecommender
            batch_size: Tamanho do mini-batch para update
        """
        self.recommender = recommender
        self.batch_size = batch_size
        self.buffer: List[Tuple] = []  # buffer de (context, arm, reward)
    
    def add_feedback(
        self,
        context: np.ndarray,
        arm: int,
        reward: float
    ):
        """
        Adiciona feedback ao buffer.
        
        Args:
            context: Vetor de contexto
            arm: Item selecionado
            reward: Recompensa
        """
        self.buffer.append((context, arm, reward))
        
        # Se atingiu batch_size, fazer update
        if len(self.buffer) >= self.batch_size:
            self.flush()
    
    def flush(self):
        """
        Processa buffer acumulado e atualiza modelo.
        """
        if not self.buffer:
            return
        
        contexts = np.array([x[0] for x in self.buffer])
        arms = np.array([x[1] for x in self.buffer])
        rewards = np.array([x[2] for x in self.buffer])
        
        self.recommender.batch_update(contexts, arms, rewards)
        self.buffer.clear()
