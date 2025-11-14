"""
Streamlit App - Página de Login
"""

import streamlit as st
import requests
from streamlit_app.config import API_URL



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
    st.Page("Home_Slate.py"),
    st.Page("Likes.py"),
    st.Page("Dislikes.py"),
    st.Page("Perfil.py"),
    st.Page(logout, title="Logout"),
    st.Page("Login.py", default=True)
]


def main():
    if "token" not in st.session_state or st.session_state.token is None:
        pg = st.navigation(user_pages, position="top")
    else:
        pg = st.navigation(user_pages, position="top")
    pg.run()


if __name__ == "__main__":
    main()
