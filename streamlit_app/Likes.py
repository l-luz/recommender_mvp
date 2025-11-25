"""
Streamlit App - Página de Likes
"""

import streamlit as st
import requests
from app.utils.config import STREAMLIT_CONFIG
from streamlit_app.components.list_feedbacks import render_feedback_card

st.set_page_config(page_title="Meus Likes", layout="wide")


def main():
    """Página de histórico de likes"""

    st.title("❤️ Meus Likes")

    # Verificar login
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("⚠️ Faça login para ver seus likes")
        st.stop()

    user_id = st.session_state.user_id

    st.write(f"Aqui estão os livros que você curtiu:")

    try:
        response = requests.get(
            f"{STREAMLIT_CONFIG["api_url"]}/feedback/user/{user_id}/likes",
            params={"user_id": user_id},
        )
        likes = response.json().get("books", [])

        if likes:
            for idx, like in enumerate(likes):
                render_feedback_card(like, idx)
        else:
            st.info("📭 Você ainda não curtiu nenhum livro")

    except Exception as e:
        st.error(f"Erro ao buscar likes: {e}")


if __name__ == "__main__":
    main()
