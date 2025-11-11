"""
Testes do recomendador (bandit contextual)
"""

import pytest
import numpy as np

from app.core.recommender import ContextualRecommender


class TestContextualRecommender:
    """Testes para ContextualRecommender"""
    
    @pytest.fixture
    def recommender(self):
        """Fixture: cria instância do recommender"""
        return ContextualRecommender(n_arms=100, context_dim=50)
    
    def test_initialization(self, recommender):
        """Testa inicialização do recommender"""
        assert recommender.n_arms == 100
        assert recommender.context_dim == 50
        assert recommender.model_type == "linucb"
    
    def test_recommend_returns_list(self, recommender):
        """Testa se recommend() retorna lista"""
        context = np.random.rand(50)
        recommendations = recommender.recommend(context, n_recommendations=4)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) == 4
    
    def test_recommend_valid_indices(self, recommender):
        """Testa se indices retornados são válidos"""
        context = np.random.rand(50)
        recommendations = recommender.recommend(context, n_recommendations=4)
        
        for idx in recommendations:
            assert 0 <= idx < recommender.n_arms
    
    def test_update_single(self, recommender):
        """Testa atualização single-shot"""
        context = np.random.rand(50)
        arm = 5
        reward = 1.0
        
        # Não deve lançar exceção
        recommender.update(context, arm, reward)
    
    def test_batch_update(self, recommender):
        """Testa atualização em batch"""
        contexts = np.random.rand(32, 50)
        arms = np.random.randint(0, 100, 32)
        rewards = np.random.rand(32)
        
        # Não deve lançar exceção
        recommender.batch_update(contexts, arms, rewards)
    
    def test_different_context_dim_raises(self):
        """Testa se context_dim diferente causa erro"""
        recommender = ContextualRecommender(n_arms=100, context_dim=50)
        context = np.random.rand(100)  # Dimensão errada
        
        # TODO: Verificar se lança exceção ou trata graciosamente
        pass
