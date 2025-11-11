"""
Rota /slate -> retorna recomendações de livros
"""

from typing import List, Optional
from pydantic import BaseModel


class BookRecommendation(BaseModel):
    """Modelo de retorno para recomendação de livro"""
    book_id: int
    title: str
    author: str
    score: float


def get_slate(user_id: int, n_items: int = 4) -> List[BookRecommendation]:
    """
    Retorna uma slate (lista) de recomendações para um usuário.
    
    Args:
        user_id: ID do usuário
        n_items: Número de itens a recomendar (padrão: 4)
    
    Returns:
        Lista de BookRecommendation
    """
    # TODO: Implementar chamada ao recommender.py (mabwiser)
    pass
