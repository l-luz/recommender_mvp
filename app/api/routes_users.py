"""
Rotas /login, /perfil -> autenticação e perfil de usuário
"""

from pydantic import BaseModel
from typing import List, Optional


class UserLogin(BaseModel):
    """Modelo de login"""
    username: str
    password: str


class UserProfile(BaseModel):
    """Modelo de perfil do usuário"""
    user_id: int
    username: str
    preferred_genres: List[str]


def login(credentials: UserLogin) -> dict:
    """
    Autentica usuário ou cria novo.
    
    Args:
        credentials: username e password
    
    Returns:
        Dict com user_id e session_token
    """
    # TODO: Implementar login/registro
    pass


def get_profile(user_id: int) -> UserProfile:
    """
    Retorna perfil do usuário.
    
    Args:
        user_id: ID do usuário
    
    Returns:
        UserProfile
    """
    # TODO: Buscar perfil do DB
    pass


def update_profile(user_id: int, profile: UserProfile) -> dict:
    """
    Atualiza perfil do usuário.
    
    Args:
        user_id: ID do usuário
        profile: Dados atualizados
    
    Returns:
        Dict confirmando atualização
    """
    # TODO: Atualizar perfil no DB
    pass
