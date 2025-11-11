"""
Geração de features de contexto (user + item)
"""

from typing import Dict, List
import numpy as np


class ContextFeatures:
    """
    Extrai e combina features de usuário e item para contexto.
    """
    
    def __init__(self, feature_dim: int = 50):
        """
        Inicializa extrator de features.
        
        Args:
            feature_dim: Dimensionalidade do vetor de contexto
        """
        self.feature_dim = feature_dim
    
    def get_user_features(self, user_id: int, db_session=None) -> np.ndarray:
        """
        Extrai features do usuário (gêneros preferidos, histórico, etc).
        
        Args:
            user_id: ID do usuário
            db_session: Sessão de DB para queries
        
        Returns:
            Vetor de features (shape: feature_dim,)
        """
        # TODO: Buscar em DB e normalizar
        pass
    
    def get_item_features(self, book_id: int, db_session=None) -> np.ndarray:
        """
        Extrai features do livro (gênero, embeddings, etc).
        
        Args:
            book_id: ID do livro
            db_session: Sessão de DB
        
        Returns:
            Vetor de features (shape: feature_dim,)
        """
        # TODO: Buscar em DB e normalizar
        pass
    
    def combine_features(
        self,
        user_features: np.ndarray,
        item_features: np.ndarray
    ) -> np.ndarray:
        """
        Combina features de usuário e item.
        
        Args:
            user_features: Features do usuário
            item_features: Features do item
        
        Returns:
            Vetor combinado de contexto
        """
        # TODO: Concatenar ou outro método de combinação
        pass
    
    def get_context(
        self,
        user_id: int,
        book_id: int,
        db_session=None
    ) -> np.ndarray:
        """
        Wrapper: retorna contexto completo user + item.
        
        Args:
            user_id: ID do usuário
            book_id: ID do livro
            db_session: Sessão de DB
        
        Returns:
            Vetor de contexto
        """
        user_feat = self.get_user_features(user_id, db_session)
        item_feat = self.get_item_features(book_id, db_session)
        return self.combine_features(user_feat, item_feat)
