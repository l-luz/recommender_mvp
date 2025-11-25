"""
Streamlit App - Página de Login
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
    pg = st.navigation(main_pages, position="sidebar")
    pg.run()


user_pages = [
    st.Page("Home_Slate.py"),
    st.Page("Likes.py"),
    st.Page("Dislikes.py"),
    st.Page("Perfil.py"),
    st.Page(logout, title="Logout"),
    st.Page("Login.py", default=True),
]


def main():
    if "token" not in st.session_state or st.session_state.token is None:
        pg = st.navigation(user_pages, position="sidebar")
    else:
        pg = st.navigation(user_pages, position="sidebar")
    pg.run()


if __name__ == "__main__":
    main()
