#!/usr/bin/env python
"""
Script principal para iniciar Streamlit + FastAPI juntos

Uso:
    python run.py
"""

import subprocess
import time
import sys
import os


def run_fastapi():
    """Inicia FastAPI em processo separado"""
    print("🚀 Iniciando FastAPI...")
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
        cwd=os.path.dirname(__file__)
    )
    time.sleep(2)  # Aguardar inicialização


def run_streamlit():
    """Inicia Streamlit"""
    print("🎨 Iniciando Streamlit...")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app/Login.py"],
        cwd=os.path.dirname(__file__)
    )


def main():
    """Inicia ambos os serviços"""
    print("=" * 50)
    print("   Recommender MVP - FastAPI + Streamlit")
    print("=" * 50)
    print()
    
    # FastAPI em background
    run_fastapi()
    
    print(f"✅ FastAPI rodando em http://127.0.0.1:8000")
    print(f"📚 Docs disponível em http://127.0.0.1:8000/docs")
    print()
    
    # Streamlit em foreground
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\n✋ Encerrando...")
        sys.exit(0)


if __name__ == "__main__":
    main()
