"""
Streamlit App - Página de Likes
"""

import streamlit as st
import requests
from app.utils.config import STREAMLIT_CONFIG

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
            params={"user_id": user_id}
        )
        likes = response.json().get("books", [])
        
        if likes:
            for like in likes:
                col1, col2, col3= st.columns([2, 4, 1])
                with col1:
                    image = like.get("image", None)
                    print(type(image))
                    if image and image != "N/A":
                        st.image(image=image, width=100)
                with col2:
                    st.write(f"**{like.get('title', 'N/A')}** - {like.get('authors', 'N/A')}")
                    st.write(f"**{like.get('genre', 'N/A')}** - {like.get('avg_rating', 'N/A')}")
                with col3:
                    if st.button("Remover", key=f"remove_{like.get('id')}"):
                        try:
                            remove_response = requests.post(
                                f"{STREAMLIT_CONFIG["api_url"]}/feedback/register",
                                json={
                                    "user_id": user_id,
                                    "book_id": like.get("id"),
                                    "action_type": "clear",
                                }
                            )
                            if remove_response.status_code == 200:
                                st.success("Livro removido dos seus likes!")
                        except Exception as e:
                            st.error(f"Erro ao remover like: {e}")
                        st.rerun()
        else:
            st.info("📭 Você ainda não curtiu nenhum livro")
    
    except Exception as e:
        st.error(f"Erro ao buscar likes: {e}")


if __name__ == "__main__":
    main()
