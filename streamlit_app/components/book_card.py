"""
Components - Book card rendering
"""

import streamlit as st
from typing import Dict
from app.utils.config import STREAMLIT_CONFIG
import requests


def _send_feedback(book_id, slate_id, pos, action):
    """
    Sends user feedback to the API and updates the session state.

    Args:
        book_id: The unique identifier of the book
        slate_id: The identifier of the recommendation slate
        pos: The position index of the book in the slate
        action: The type of action
    """
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
    Renders a book card in Streamlit.

    Args:
        book: Dictionary with book data
        idx: Index for page unique key
        slate_idx: the slate identifier
    """
    col_img, col_info = st.columns([1, 3])

    with col_img:
        image = book.get("image", None)
        try:
            if image and image != "N/A":
                st.image(image=image, width=100)
            else:
                raise Exception()
        except:
            st.write(f"📖")


    with col_info:
        st.write(f"**{book.get('title', 'N/A')}**")
        st.caption(f"por {book.get('authors', 'N/A')}")
        with st.expander("Description"):
            st.write(f"**{book.get("description", 'N/A')}**")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rating\n", f"⭐{book.get('score', 0):}/5.0")

        with col2:

            st.write(f"Gênero: {book.get('categories', 'N/A')}")

        foot1, foot2 = st.columns(2)
        book_id = book.get("book_id")
        with foot1:
            st.button(
                "👍 Like",
                key=f"like-{idx}",
                on_click=_send_feedback,
                args=(book_id, slate_idx, idx, "like"),
            )

        with foot2:
            st.button(
                "👎 Dislike",
                key=f"dislike-{idx}",
                on_click=_send_feedback,
                args=(book_id, slate_idx, idx, "dislike"),
            )
