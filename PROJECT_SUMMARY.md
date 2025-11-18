## 📋 Resumo do Projeto

### Backend (FastAPI) - `app/`
```
app/
├── main.py                    # Entry point FastAPI
├── api/
│   ├── routes_slate.py       # GET /slate (recomendações)
│   ├── routes_feedback.py    # POST /feedback (like/dislike)
│   ├── routes_users.py       # POST /login, GET/PUT /profile
│   └── schemas.py            # API request/response validation
├── core/
│   ├── recommender/ 
│   │   ├── base.py           # BaseRecommender (Interface)
│   │   └── linucb.py         # LinUCBRecommender (Linucb)
│   ├── training.py           # OnlineTrainer (mini-batch)
│   └── context_features.py   # Extrator de features (user+item)
├── db/
│   ├── database.py           # SQLite + SessionLocal
│   ├── models.py             # Tabelas (User, Book, Event, Category, Author, etc)
│   └── crud.py               # Operações CRUD
└── utils/
    ├── config.py             # Configurações globais
    ├── logger.py             # Logging de eventos # TODO: verify
    └── seeds.py              # Gerador de dados teste
```

### Frontend (Streamlit) - `streamlit_app/`
```
streamlit_app/
├── __init__.py               # Inicialização
├── config.py                 # Configurações globais
├── Login.py                  # Autenticação
├── Home_Slate.py            # Recomendações
├── Likes.py                 # Histórico de likes
├── Dislikes.py              # Histórico de dislikes
├── Perfil.py                # Preferências do usuário
└── components/
    ├── book_card.py         # Renderização de livros
    └── navigation.py        # Menu compartilhado # TODO: use?
```
# TODO: review in the end
<!-- ### Testes - `tests/`
```
tests/
├── test_api.py              # Testes das rotas FastAPI
├── test_recommender.py      # Testes do modelo (mabwiser)
├── test_db.py               # Testes CRUD + DB
└── conftest.py              # Fixtures pytest
``` -->

### Dados e Análise - `data/` e `notebooks/`
```
data/
├── raw/                      # CSVs originais
│   ├── books_data.csv        
│   └── books_rating.csv
├── processed/                # Dados limpos
│   └── books_cleaned.csv
│   └── rating_cleaned.csv
└── embeddings/               # TF-IDF / Sentence-Transformers

notebooks/
└── data_extraction.ipynb    # Clean data and populate db
<!-- ├── offline_eval.ipynb       # CTR, Regret, Diversidade
└── exploration_tests.ipynb  # Testes de exploração -->
```

---

## 📦 Arquivos de Configuração

- **`requirements.txt`** - Dependências (streamlit, fastapi, sqlalchemy, mabwiser, pytest, etc)
- **`run.py`** - Script para iniciar FastAPI + Streamlit
- **`README.md`** - Documentação completa do projeto
- **`.gitignore`** - Configuração Git (venv, __pycache__, .db, etc)
- **`.streamlit/config.toml`** - Configuração Streamlit

---

## Quickstart

### 1. Ativar Virtual Environment
```powershell
venv\Scripts\Activate.ps1
```

### 2. Instalar Dependências
```powershell
pip install -r requirements.txt
```

### 3. Executar Projeto
```powershell
# Opção 1: Automático (ambos os serviços)
python run.py

# Opção 2: Manual em terminais separados
# Terminal 1:
uvicorn app.main:app --reload

# Terminal 2:
streamlit run streamlit_app/Login.py
```

### 4. Acessar Aplicação
- **Streamlit**: http://localhost:8501
- **FastAPI**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

---

## 🧠 Modelo de Recomendação

- **Algoritmo**: LinUCB (Linear Upper Confidence Bound)
- **Biblioteca**: MABWiser
- **Contexto**: Features de usuário + features de item
- **Aprendizado**: Online com mini-batches
- **Exploração**: Balanceada com parâmetro alpha

---

## 📊 Funcionalidades Implementadas

✅ Estrutura completa de pastas  
✅ Modelos SQLAlchemy (User, Book, Event, Review)  
✅ Rotas FastAPI (slate, feedback, login, profile)  
✅ Páginas Streamlit (Login, Home, Likes, Dislikes, Perfil, Logout)  
✅ Lógica do recomendador (stub para mabwiser)  
✅ Trainer online com mini-batch  
✅ Extrator de features de contexto  
✅ Testes pytest (fixtures, CRUD, API)  
✅ Notebooks Jupyter para análise offline  
✅ Logging e seeding de dados  
✅ Documentação e README  

---

## 🔧 Itens TODO

- [ ] Implementar contexto_features.py (extração real)
- [ ] Implementar recommender.py (integrar mabwiser)
- [ ] Conectar rotas FastAPI
- [ ] Conectar Streamlit com API
- [ ] Dataset de livros/usuários
- [ ] Gerar embeddings
- [ ] Testes end-to-end
- [ ] Dashboard de métricas
- [ ] Autenticação JWT
- [ ] Deploy em cloud

---

## 📝 Notas

- **Banco**: SQLite em `data/database.db`
- **Logs**: `logs/app_*.log`
- **Session**: Streamlit session_state
- **Ambiente**: venv Python 3.9+
- **PEP8**: Código segue padrões Python

---

**Projeto criado em**: 11 de Novembro de 2025  
