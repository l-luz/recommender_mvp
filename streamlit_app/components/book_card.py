"""
Components - Renderização de card de livro
"""

import streamlit as st
from typing import Dict
from app.utils.config_streamlit import STREAMLIT_CONFIG["api_url"]
import requests


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
        else:
            st.write("📖")  # TODO: Use a placeholder

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

        with foot1:
            if st.button(f"👍 Like", key=f"like_{idx}"):
                try:
                    response = requests.post(
                        f"{STREAMLIT_CONFIG["api_url"]}/feedback/register",
                        json={
                            "user_id": user_id,
                            "book_id": book.get("book_id"),
                            "slate_id": slate_idx,
                            "action_type": "like",
                            "pos": idx,
                        },
                    )
                    if response.status_code == 200:
                        st.success("Adicionado aos seus likes!")
                except Exception as e:
                    st.error(f"Erro ao enviar feedback: {e}")

        with foot2:
            if st.button(f"👎 Dislike", key=f"dislike_{idx}"):
                try:
                    response = requests.post(
                        f"{STREAMLIT_CONFIG["api_url"]}/feedback/register",
                        json={
                            "user_id": user_id,
                            "book_id": book.get("book_id"),
                            "slate_id": slate_idx,
                            "action_type": "dislike",
                            "pos": idx,
                        },
                    )
                    if response.status_code == 200:
                        st.success("Adicionado aos seus dislikes!")
                        st.info("Ok, não recomendaremos similar a este")
                except Exception as e:
                    st.error(f"Erro ao enviar feedback: {e}")
