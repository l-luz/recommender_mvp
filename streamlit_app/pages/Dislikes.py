"""
Streamlit App - Página de Dislikes
"""

import streamlit as st
import requests

from streamlit_app.config import API_URL

st.set_page_config(page_title="Meus Dislikes", layout="wide")


def main():
    """Página de histórico de dislikes"""
    
    st.title("👎 Meus Dislikes")
    
    # Verificar login
    if "user_id" not in st.session_state:
        st.warning("⚠️ Faça login para ver seus dislikes")
        st.stop()    
    user_id = st.session_state.user_id
    
    st.write(f"Livros que você não curtiu:")
    
    try:
        response = requests.get(
             f"{API_URL}/events",
            json={"user_id": user_id, "event_type": "dislike"}
        )

        dislikes = []  # response.json().get("events", [])
        
        if dislikes:
            for dislike in dislikes:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📖 **{dislike.get('title', 'N/A')}** - {dislike.get('author', 'N/A')}")
                with col2:
                    if st.button("Remover", key=f"remove_{dislike.get('id')}"):
                        # TODO: Remover dislike
                        st.rerun()
        else:
            st.info("✅ Você não marcou nenhum livro como dislike ainda")
    
    except Exception as e:
        st.error(f"Erro ao buscar dislikes: {e}")


if __name__ == "__main__":
    main()
