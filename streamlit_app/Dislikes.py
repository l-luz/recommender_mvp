"""
Streamlit App - Página de Dislikes
"""

import streamlit as st
import requests
from app.utils.config import STREAMLIT_CONFIG
from streamlit_app.components.list_feedbacks import render_feedback_card

st.set_page_config(page_title="Meus Dislikes", layout="wide")


def main():
    """Página de histórico de dislikes"""

    st.title("👎 Meus Dislikes")

    # Verificar login
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("⚠️ Faça login para ver seus dislikes")
        st.stop()
    user_id = st.session_state.user_id

    st.write(f"Livros que você não curtiu:")

    try:
        response = requests.get(
            f"{STREAMLIT_CONFIG["api_url"]}/feedback/user/{user_id}/dislikes",
            params={"user_id": user_id},
        )
        dislikes = response.json().get("books", [])

        if dislikes:
            for idx, dislike in enumerate(dislikes):
                render_feedback_card(dislike, idx)
            
        else:
            st.info("✅ Você não marcou nenhum livro como dislike ainda")

    except Exception as e:
        st.error(f"Erro ao buscar dislikes: {e}")


if __name__ == "__main__":
    main()
