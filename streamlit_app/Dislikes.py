"""
Streamlit App - Página de Dislikes
"""

import streamlit as st
import requests
from app.utils.config import STREAMLIT_CONFIG

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
            params={"user_id": user_id}
        )
        dislikes = response.json().get("events", [])
        
        if dislikes:
            for dislike in dislikes:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📖 **{dislike.get('title', 'N/A')}** - {dislike.get('author', 'N/A')}")
                with col2:
                    if st.button("Remover", key=f"remove_{dislike.get('id')}"):
                        try:
                            like_response = requests.post(
                                f"{STREAMLIT_CONFIG["api_url"]}/feedback/register",
                                json={
                                    "user_id": user_id,
                                    "book_id": dislike.get("id"),
                                    "action": "clear"
                                }
                            )
                            if like_response.status_code == 200:
                                st.success("Livro removido dos seus dislikes!")
                        except Exception as e:
                            st.error(f"Erro ao remover dislike: {e}")
                        # st.rerun()
        else:
            st.info("✅ Você não marcou nenhum livro como dislike ainda")
    
    except Exception as e:
        st.error(f"Erro ao buscar dislikes: {e}")


if __name__ == "__main__":
    main()
