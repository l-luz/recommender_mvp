"""
Init file for streamlit app
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar projeto ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configurar página padrão
st.set_page_config(
    page_title="Recommender MVP",
    page_icon="📚",
    layout="wide",
)

# Inicializar session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.token = None
