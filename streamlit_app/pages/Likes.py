"""
Streamlit App - Página de Likes
"""

import streamlit as st
import requests

st.set_page_config(page_title="Meus Likes", layout="wide")


def main():
    """Página de histórico de likes"""
    
    st.title("❤️ Meus Likes")
    
    # Verificar login
    if "user_id" not in st.session_state:
        st.warning("⚠️ Faça login para ver seus likes")
        st.stop()
    
    user_id = st.session_state.user_id
    
    st.write(f"Aqui estão os livros que você curtiu:")
    
    try:
        # TODO: Fazer request para /events?user_id=X&event_type=like
        likes = []  # response.json().get("events", [])
        
        if likes:
            for like in likes:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📖 **{like.get('title', 'N/A')}** - {like.get('author', 'N/A')}")
                with col2:
                    if st.button("Remover", key=f"remove_{like.get('id')}"):
                        # TODO: Remover like
                        st.rerun()
        else:
            st.info("📭 Você ainda não curtiu nenhum livro")
    
    except Exception as e:
        st.error(f"Erro ao buscar likes: {e}")


if __name__ == "__main__":
    main()
