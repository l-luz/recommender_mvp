"""
Streamlit App - Página principal (Slate de livros)
"""

import streamlit as st
import requests
from typing import List, Dict
from streamlit_app.components.book_card import render_book_card
from streamlit_app.config import API_URL

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


def main():
    """Página principal de recomendações"""

    st.title("📚 Recomendações Personalizadas")
    st.write("Descubra novos livros baseado em suas preferências")

    # Verificar login
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("⚠️ Faça login para ver recomendações")
        st.stop()

    user_id = st.session_state.user_id
    st.success(f"Bem-vindo, {st.session_state.get('username', f'User {user_id}')}!")

    # Buscar recomendações
    st.subheader("Suas recomendações de hoje:")

    try:
        response = requests.post(
            f"{API_URL}/slate/recommend", params={"user_id": user_id, "n_items": 4}
        )
        recommendations = response.json().get("recommendations", [])
        slate_id = response.json().get("slate_id", None)
    except Exception as e:
        st.error(f"Erro ao buscar recomendações: {e}")
        recommendations = []

    # Exibir cards de livros
    if recommendations:
        cols = st.columns(2)
        for idx, book in enumerate(recommendations):
            with cols[idx % 2]:
                render_book_card(book, idx, slate_id)
    else:
        st.info("📭 Nenhuma recomendação disponível no momento")

    if st.button("🔄 Atualizar recomendações"):
        st.rerun()


if __name__ == "__main__":
    main()
