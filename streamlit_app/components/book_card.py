"""
Components - Renderização de card de livro
"""

import streamlit as st
from typing import Dict


def render_book_card(book: Dict, idx: int):
    """
    Renderiza um card de livro em Streamlit.
    
    Args:
        book: Dicionário com dados do livro
        idx: Índice para key unique
    """
    
    col_img, col_info = st.columns([1, 3])
    
    with col_img:
        st.write("📖")  # Placeholder para imagem
    
    with col_info:
        st.write(f"**{book.get('title', 'N/A')}**")
        st.caption(f"por {book.get('author', 'N/A')}")
        st.write(book.get('description', 'Sem descrição'))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Score", f"{book.get('score', 0):.2f}")
        
        with col2:
            st.write(f"Gênero: {book.get('genre', 'N/A')}")
        
        with col3:
            st.write(f"Rating: ⭐ {book.get('rating', 0)}/5")
