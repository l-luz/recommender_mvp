"""
Streamlit App - Página principal (Slate de livros)
"""

import streamlit as st
import requests
from typing import List, Dict
from app.utils.config import STREAMLIT_CONFIG
from streamlit_app.components.book_card import render_book_card

# Configurar página
st.set_page_config(
    page_title="Recommender MVP - Home", layout="wide", initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown(
    """
    <style>
    .book-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def fetch_slate(user_id):
    try:
        resp = requests.post(
            f"{STREAMLIT_CONFIG['api_url']}/slate/recommend",
            params={"user_id": user_id, "n_items": STREAMLIT_CONFIG["max_recommendations"]},
        )
        resp.raise_for_status()
        data = resp.json()
        st.session_state.slate = {
            "recommendations": data.get("recommendations", []),
            "slate_id": data.get("slate_id"),
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar recomendações: {e}")
        st.session_state.slate = {"recommendations": [], "slate_id": None}


def main():
    """Página principal de recomendações"""

    st.title("📚 Recomendações Personalizadas")
    st.write("Descubra novos livros baseado em suas preferências")

    # Verify login
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("⚠️ Faça login para ver recomendações")
        st.stop()

    user_id = st.session_state.user_id
    st.success(f"Bem-vindo, {st.session_state.get('username', f'User {user_id}')}!")
    st.subheader("Suas recomendações de hoje:")

    if "slate" not in st.session_state or st.button("🔄 Atualizar recomendações"):
        with st.spinner("Buscando novas recomendações..."):
            fetch_slate(user_id)
        st.rerun()

    slate = st.session_state.get("slate", {})
    recommendations = slate.get("recommendations", [])
    slate_id = slate.get("slate_id")

    if recommendations:
        cols = st.columns(2)
        for idx, book in enumerate(recommendations):
            with cols[idx % 2]:
                render_book_card(book, idx, slate_id)
    else:
        st.info("📭 Nenhuma recomendação disponível no momento.")
        if st.button("🔎 Tentar buscar novamente"):
            with st.spinner("Buscando..."):
                fetch_slate(user_id)
            st.rerun()


if __name__ == "__main__":
    main()
