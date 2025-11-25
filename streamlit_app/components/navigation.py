"""
Components - Navegação/header compartilhado
"""

import streamlit as st

main_pages = [
    st.Page("Login.py", default=True),
]


def logout():
    """Logout do usuário"""
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.token = None
    st.success("✅ Logout realizado com sucesso!")
    import time

    time.sleep(1)
    pg = st.navigation(main_pages, position="top")
    pg.run()


user_pages = [
    st.Page("Home_Slate.py", default=True),
    st.Page("Likes.py"),
    st.Page("Dislikes.py"),
    st.Page("Perfil.py"),
    st.Page(logout, title="Logout"),
]


def render_navigation():
    """
    Renderiza navegação/header da aplicação.
    """

    with st.sidebar:
        st.title("📚 Recommender MVP")
        st.markdown("---")

        if st.session_state.user_id is not None:
            st.write(f"**Usuário:** {st.session_state.get('username', 'N/A')}")
            st.write(f"**ID:** {st.session_state.get('user_id', 'N/A')}")
            st.markdown("---")

            # Menu de navegação
            st.subheader("Menu")

            menu_options = {
                "🏠 Home": "Home_Slate.py",
                "❤️ Likes": "Likes.py",
                "👎 Dislikes": "Dislikes.py",
                "👤 Perfil": "Perfil.py",
                "🚪 Logout": logout,
            }

            for label, page in menu_options.items():
                if st.button(label, use_container_width=True):
                    st.navigation(f"{page}")

        else:
            st.info("📲 Faça login para continuar")
            if st.button("Ir para Login", use_container_width=True):
                st.navigation("Login.py")
