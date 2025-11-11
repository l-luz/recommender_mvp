#!/usr/bin/env python3
"""
QUICKSTART - Guia de Início Rápido do Projeto

Execute este arquivo para entender a estrutura do projeto.
"""

import os
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def main():
    root = Path(__file__).parent
    
    print_header("🚀 RECOMMENDER MVP - QUICKSTART")
    
    print("""
    📚 Bem-vindo ao Recommender MVP!
    
    Este é um projeto de recomendação de livros com:
    - FastAPI para backend
    - Streamlit para frontend
    - SQLite para persistência
    - MABWiser para aprendizado por reforço contextual
    
    """)
    
    print_header("1️⃣ SETUP INICIAL")
    
    print("""
    1. Ativar Virtual Environment:
    
       Windows (PowerShell):
       venv\\Scripts\\Activate.ps1
       
       Windows (CMD):
       venv\\Scripts\\activate.bat
       
       Mac/Linux:
       source venv/bin/activate
    
    2. Instalar dependências:
    
       pip install -r requirements.txt
    """)
    
    print_header("2️⃣ EXECUTAR PROJETO")
    
    print("""
    Opção A - Automático (RECOMENDADO):
    
       python run.py
       
       Inicia FastAPI + Streamlit automaticamente
    
    Opção B - Manual em terminais separados:
    
       Terminal 1 (FastAPI):
       uvicorn app.main:app --reload
       
       Terminal 2 (Streamlit):
       streamlit run streamlit_app/Login.py
    """)
    
    print_header("3️⃣ ACESSAR APLICAÇÃO")
    
    print("""
    Após iniciar:
    
    🌐 Frontend Streamlit:
       http://localhost:8501
    
    🔌 Backend FastAPI:
       http://127.0.0.1:8000
    
    📖 Documentação Interativa:
       http://127.0.0.1:8000/docs
    """)
    
    print_header("4️⃣ ESTRUTURA DO PROJETO")
    
    print(f"""
    {root.name}/
    ├── app/                    Backend FastAPI
    │   ├── main.py            Entry point
    │   ├── api/               Rotas (slate, feedback, users)
    │   ├── core/              Lógica do recomendador
    │   ├── db/                Modelos e CRUD
    │   └── utils/             Config, logging, seeds
    │
    ├── streamlit_app/          Frontend Streamlit
    │   ├── Login.py           Autenticação
    │   ├── Home_Slate.py      Recomendações
    │   ├── Likes.py           Histórico
    │   ├── Perfil.py          Preferências
    │   └── components/        Componentes reutilizáveis
    │
    ├── tests/                 Testes Pytest
    │   ├── test_api.py        Testes API
    │   ├── test_recommender.py Testes do modelo
    │   └── test_db.py         Testes CRUD
    │
    ├── data/                  Dados
    │   ├── raw/              CSV originais
    │   ├── processed/        Dados limpos
    │   └── embeddings/       Features
    │
    ├── notebooks/            Jupyter Notebooks
    │   ├── offline_eval.ipynb Análise
    │   └── exploration_tests.ipynb Testes
    │
    ├── requirements.txt       Dependências
    ├── run.py                 Script de inicialização
    └── README.md              Documentação
    """)
    
    print_header("5️⃣ PRÓXIMOS PASSOS")
    
    print("""
    ✅ Estrutura pronta! Agora você pode:
    
    1. Explorar app/core/recommender.py
       → Implementar integração com MABWiser
    
    2. Completar app/core/context_features.py
       → Adicionar extração real de features
    
    3. Conectar rotas FastAPI
       → Ligar APIs ao frontend Streamlit
    
    4. Criar dataset de livros
       → Popular data/raw/ com CSVs
    
    5. Gerar embeddings
       → Usar TF-IDF ou Sentence-Transformers
    
    6. Rodar testes
       pytest tests/ -v
    
    7. Analisar offline
       jupyter notebook notebooks/offline_eval.ipynb
    """)
    
    print_header("6️⃣ DOCUMENTAÇÃO")
    
    print("""
    📖 Veja arquivos para mais info:
    
    - README.md              Documentação completa
    - PROJECT_SUMMARY.md     Resumo do projeto
    - instructions.md        Instruções originais
    - Docstrings nos .py     Comentários inline
    """)
    
    print_header("⚡ COMANDO RÁPIDO")
    
    print("""
    Pronto para começar? Execute:
    
    python run.py
    
    E acesse: http://localhost:8501
    """)
    
    print("\n✨ Bom desenvolvimento! 🚀\n")

if __name__ == "__main__":
    main()
