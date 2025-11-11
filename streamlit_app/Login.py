"""
Streamlit App - Página de Login
"""

import streamlit as st
import requests

st.set_page_config(page_title="Login", layout="centered")


def main():
    """Página de login"""
    
    st.title("🔐 Login")
    
    # Formulário de login
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        submitted = st.form_submit_button("Entrar")
    
    if submitted:
        if not username or not password:
            st.error("❌ Preencha usuário e senha!")
            return
        
        try:
            # TODO: Fazer request para /login
            response = requests.post(
                "http://127.0.0.1:8000/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.user_id = data.get("user_id")
                st.session_state.username = username
                st.session_state.token = data.get("token")
                
                st.success(f"✅ Bem-vindo, {username}!")
                st.balloons()
                
                # Redirecionar
                import time
                time.sleep(1)
                st.switch_page("pages/Home_Slate.py")
            else:
                st.error("❌ Usuário ou senha incorretos")
        
        except Exception as e:
            st.error(f"❌ Erro ao conectar: {e}")
    
    # Link para registrar
    st.markdown("---")
    st.write("Não tem conta? Crie uma agora!")
    
    with st.form("register_form"):
        new_username = st.text_input(
            "Novo usuário",
            placeholder="Escolha um nome de usuário",
            key="register_username"
        )
        new_password = st.text_input(
            "Senha",
            type="password",
            placeholder="Escolha uma senha",
            key="register_password"
        )
        confirm_password = st.text_input(
            "Confirmar senha",
            type="password",
            placeholder="Confirme sua senha",
            key="confirm_password"
        )
        
        register_submitted = st.form_submit_button("Registrar")
    
    if register_submitted:
        if not new_username or not new_password:
            st.error("❌ Preencha todos os campos!")
            return
        
        if new_password != confirm_password:
            st.error("❌ Senhas não conferem!")
            return
        
        try:
            # TODO: Fazer request para /register
            st.success(f"✅ Usuário {new_username} registrado com sucesso! Faça login.")
        except Exception as e:
            st.error(f"❌ Erro ao registrar: {e}")


if __name__ == "__main__":
    main()
