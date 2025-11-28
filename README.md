# Recommender MVP

> **MVP de recomendação de livros com aprendizado por reforço contextual**

MVP de recomendação de livros usando bandido contextual (LinUCB), com backend FastAPI e frontend Streamlit. Banco local em SQLite via SQLAlchemy e notebooks para análises offline.

## Visão Geral
- Backend: FastAPI com endpoints para recomendações e feedback.
- Frontend: Streamlit para login, navegação e interação com recomendações.
- Modelo: LinUCB com features de contexto (usuário + item) e atualização online em mini-batches.
- Persistência: SQLite em `data/database.db`.
- Notebooks: experimentos de extração de dados, features e testes de exploração.

## Estrutura do Projeto
recommender_mvp/
├── app/ # Backend FastAPI
│ ├── api/ # Rotas e schemas
│ ├── core/ # Recomendador (LinUCB), features, runtime
│ ├── db/ # Models, CRUD, conexão
│ └── utils/ # Configurações e utilidades
├── streamlit_app/ # Frontend Streamlit
├── data/ # Banco SQLite e artefatos
├── notebooks/ # Análises Jupyter
├── tests/ # Testes pytest
├── run.py # Sobe API + Streamlit
└── requirements.txt


## Pré-requisitos
- Python 3.10+
- SQLite
- (Opcional) virtualenv/venv

## Setup Rápido
### 1. Configurar Ambiente

```bash
# Criar virtual environment
python -m venv venv

# Ativar virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar Ambos os Serviços

```bash
# Opção 1: Script conveniente (recomendado)
python run.py

# Opção 2: Manualmente em terminais separados
# Terminal 1 - FastAPI
uvicorn app.main:app --reload

# Terminal 2 - Streamlit
streamlit run streamlit_app/Login.py
```

### 3. Acessar Aplicação
Streamlit: http://localhost:8501
FastAPI: http://127.0.0.1:8000
Docs Swagger: http://127.0.0.1:8000/docs

## Configuração
> **Edite app/utils/config.py para ajustar:**
- Caminhos de dados (DATA_DIR, DATABASE_PATH)
- Hiperparâmetros do LinUCB (alpha, feature_dim, batch_size)
- Parâmetros de API/Streamlit (host, port, api_url, max_recommendations)

## Notebooks
- **data_extraction.ipynb:** extração/visualização de dados.
- **build_item_features.ipynb:** construção de features de itens.
- **exploration_tests.ipynb:** simulações de exploração (LinUCB vs random).

## Testes
```batch
pytest
# ou com cobertura
pytest --cov=app
```
