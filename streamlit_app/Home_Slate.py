"""
Streamlit App - Página principal (Slate de livros)
"""

import streamlit as st
import requests
from typing import List, Dict

# Configurar página
st.set_page_config(
    page_title="Recommender MVP - Home",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
    <style>
    .book-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Página principal de recomendações"""
    
    st.title("📚 Recomendações Personalizadas")
    st.write("Descubra novos livros baseado em suas preferências")
    
    # Verificar login
    if "user_id" not in st.session_state:
        st.warning("⚠️ Faça login para ver recomendações")
        st.stop()
    
    user_id = st.session_state.user_id
    st.success(f"Bem-vindo, {st.session_state.get('username', f'User {user_id}')}!")
    
    # Buscar recomendações
    st.subheader("Suas recomendações de hoje:")
    
    try:
        # TODO: Fazer request para /slate
        response = requests.post(
            "http://127.0.0.1:8000/slate",
            params={"user_id": user_id, "n_items": 4}
        )
        recommendations = response.json().get("recommendations", [])
    except Exception as e:
        st.error(f"Erro ao buscar recomendações: {e}")
        recommendations = []
    
    # Exibir cards de livros
    if recommendations:
        cols = st.columns(2)
        for idx, book in enumerate(recommendations):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="book-card">
                        <h3>{book.get('title', 'N/A')}</h3>
                        <p><strong>Autor:</strong> {book.get('author', 'N/A')}</p>
                        <p><strong>Gênero:</strong> {book.get('genre', 'N/A')}</p>
                        <p>{book.get('description', 'Sem descrição')}</p>
                        <p><strong>Score:</strong> {book.get('score', 0):.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"👍 Like", key=f"like_{idx}"):
                        # TODO: Enviar feedback
                        st.success("Adicionado aos seus likes!")
                
                with col2:
                    if st.button(f"👎 Dislike", key=f"dislike_{idx}"):
                        # TODO: Enviar feedback
                        st.info("Ok, não recomendaremos similar a este")
    else:
        st.info("📭 Nenhuma recomendação disponível no momento")
    
    # Sidebar com opções
    with st.sidebar:
        st.subheader("Opções")
        if st.button("🔄 Atualizar recomendações"):
            st.rerun()


if __name__ == "__main__":
    main()
