"""
Components - Renderização de card de livro
"""

import streamlit as st
from typing import Dict
from app.utils.config import STREAMLIT_CONFIG
import requests

def send_feedback(book_id, slate_id, pos, action):
    try:
        requests.post(
            f"{STREAMLIT_CONFIG['api_url']}/feedback/register",
            json={
                "user_id": st.session_state.user_id,
                "book_id": book_id,
                "slate_id": slate_id,
                "pos": pos,
                "action_type": action,
            },
            timeout=5,
        ).raise_for_status()
        if "slate" in st.session_state:
            del st.session_state["slate"]

    except Exception as e:
        st.error(f"Erro ao enviar feedback: {e}")

def render_book_card(book: Dict, idx: int, slate_idx: int):
    """
    Renderiza um card de livro em Streamlit.

    Args:
        book: Dicionário com dados do livro
        idx: Índice para key unique
    """
    user_id = st.session_state.user_id
    col_img, col_info = st.columns([1, 3])

    with col_img:
        image = book.get("image", None)
        if image and image != "N/A":
            st.image(image=image, width=100)

    with col_info:
        st.write(f"**{book.get('title', 'N/A')}**")
        st.caption(f"por {book.get('authors', 'N/A')}")
        st.write(book.get("description", "Sem descrição")[:100])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Score", f"{book.get('score', 0):.2f}")

        with col2:

            st.write(f"Gênero: {book.get('genre', 'N/A')}")

        with col3:
            st.write(f"Rating: ⭐ {book.get('rating', 0)}/5")

        foot1, foot2 = st.columns(2)
        book_id = book.get("book_id")
        with foot1:
            st.button("👍 Like", key=f"like-{idx}", on_click=send_feedback, args=(book_id, slate_idx, idx, "like"))

        with foot2:
            st.button("👎 Dislike", key=f"dislike-{idx}", on_click=send_feedback, args=(book_id, slate_idx, idx, "dislike"))