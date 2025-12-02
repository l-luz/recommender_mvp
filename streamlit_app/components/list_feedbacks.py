"""
Components - Feedback cards rendering
"""

from typing import Dict

import streamlit as st
import requests
from app.utils.config import STREAMLIT_CONFIG

st.set_page_config(page_title="Meus Likes", layout="wide")


def _remove_feedback(book_id):
    """
    Removes previously sent feedback for a specific book.

    Args:
        book_id: The unique identifier of the book
    """
    try:
        remove_response = requests.post(
            f"{STREAMLIT_CONFIG["api_url"]}/feedback/register",
            json={
                "user_id": st.session_state.user_id,
                "book_id": book_id,
                "action_type": "clear",
            },
        )
        if remove_response.status_code == 200:
            st.success("Feedback removido!")
    except Exception as e:
        st.error(f"Erro ao remover feedback: {e}")


def render_feedback_card(book: Dict, idx: int):
    """
    Renders a feedback card in Streamlit.

    Args:
    book: Dictionary with book data
    idx: Index for unique key
    """
    col1, col2, col3 = st.columns([2, 4, 1])
    with col1:
        image = book.get("image", None)
        try:
            if image and image != "N/A":
                st.image(image=image, width=100)
            else:
                raise Exception()
        except:
            st.write(f"📖")
    with col2:
        st.write(f"**{book.get('title', 'N/A')}** - {book.get('authors', 'N/A')}")
        st.write(
            f"**{book.get('categories', 'N/A')}** - {book.get('avg_rating', 'N/A')}"
        )
        with st.expander("Description"):
            st.write(f"**{book.get('description', 'N/A')}**")

    with col3:
        book_id = book.get("id")
        st.button(
            "Remover",
            key=f"remove_{idx}",
            on_click=_remove_feedback,
            args=(book_id,),
        )
