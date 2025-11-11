"""
Components - Navegação/header compartilhado
"""

import streamlit as st


def render_navigation():
    """
    Renderiza navegação/header da aplicação.
    """
    
    with st.sidebar:
        st.title("📚 Recommender MVP")
        st.markdown("---")
        
        if "user_id" in st.session_state:
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
                "🚪 Logout": "Logout.py",
            }
            
            for label, page in menu_options.items():
                if st.button(label, use_container_width=True):
                    st.switch_page(f"pages/{page}")
        
        else:
            st.info("📲 Faça login para continuar")
            if st.button("Ir para Login", use_container_width=True):
                st.switch_page("pages/Login.py")
