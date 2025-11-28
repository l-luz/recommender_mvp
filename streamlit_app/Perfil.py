"""
Streamlit App - Página de Perfil
"""

import streamlit as st
import requests
from app.utils.config import STREAMLIT_CONFIG

st.set_page_config(page_title="Meu Perfil", layout="wide")


def main():
    """Página de perfil do usuário"""

    st.title("👤 Meu Perfil")

    # Verificar login
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.warning("⚠️ Faça login para acessar seu perfil")
        st.stop()

    user_id = st.session_state.user_id
    username = st.session_state.get("username", f"User {user_id}")

    st.subheader(f"Bem-vindo, {username}!")

    try:
        genre_response = requests.get(
            f"{STREAMLIT_CONFIG["api_url"]}/users/genres",
        )

        user_response = requests.get(
            f"{STREAMLIT_CONFIG["api_url"]}/users/profile/{user_id}",
            json={"id": user_id},
        )

        genres_options = genre_response.json().get("categories", [])

        st.write("**Gêneros Preferidos:**")

        user_genres = user_response.json().get("preferred_genres") or []

        with st.form("preferences_form"):
            selected_genres = st.multiselect(
                "Selecione seus gêneros preferidos:",
                options=genres_options,
                default=user_genres,
            )

            submitted = st.form_submit_button("Salvar Preferências")

            if submitted:
                try:
                    update_response = requests.put(
                        f"{STREAMLIT_CONFIG["api_url"]}/users/profile/{user_id}",
                        json={
                            "id": user_id,
                            "username": username,
                            "preferred_genres": selected_genres,
                        },
                    )
                    if update_response.status_code == 200:
                        st.success("✅ Preferências atualizadas!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao atualizar preferências: {e}")

        st.divider()

        # Estatísticas
        st.subheader("📊 Suas Estatísticas")
        col1, col2, col3 = st.columns(3)
        likes = user_response.json().get("likes", 0)
        dislikes = user_response.json().get("dislikes", 0)
        unique_interactions = user_response.json().get("unique_books_interacted", 0)
        with col1:
            st.metric("Likes", likes)

        with col2:
            st.metric("Dislikes", dislikes)

        with col3:
            st.metric("Livros Explorados", unique_interactions)

    except Exception as e:
        st.error(f"Erro ao carregar perfil: {e}")


if __name__ == "__main__":
    main()
