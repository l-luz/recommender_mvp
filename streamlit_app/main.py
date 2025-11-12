"""
Streamlit App - Página de Login
"""

import streamlit as st
import requests

from streamlit_app.config import API_URL

st.set_page_config(page_title="Login", layout="centered")


def main():
    if not st.session_state.get("user_id"):
        st.switch_page("pages/Login.py")
    else:
        st.switch_page("pages/Home_Slate.py")    


if __name__ == "__main__":
    main()
