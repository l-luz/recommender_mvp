"""
Init file for streamlit app
"""

import streamlit as st
import sys
from pathlib import Path

from app.utils.config import STREAMLIT_CONFIG

# Adicionar projeto ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configurar página padrão
st.set_page_config(
    page_title=STREAMLIT_CONFIG["page_title"],
    page_icon="📚",
    layout=STREAMLIT_CONFIG["layout"],
)

# Inicializar session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.token = None
