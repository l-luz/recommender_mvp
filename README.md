# Recommender MVP

> **MVP de recomendação de livros com aprendizado por reforço contextual**

## 📋 Visão Geral

Sistema de recomendação de livros utilizando:
- **FastAPI** para backend
- **Streamlit** para frontend
- **SQLite + SQLAlchemy** para persistência
- **MABWiser** para aprendizado por reforço contextual (LinUCB)
- **pandas + scikit-learn** para processamento de dados

## 🏗️ Estrutura do Projeto

```
recommender_mvp/
├── app/                    # Backend FastAPI
│   ├── api/               # Rotas da API
│   ├── core/              # Lógica de recomendação (MABWiser)
│   ├── db/                # Modelos e CRUD SQLAlchemy
│   ├── utils/             # Configurações, logging, seeds
│   └── main.py            # Entry point FastAPI
├── streamlit_app/         # Frontend Streamlit
│   ├── Login.py           # Autenticação
│   ├── Home_Slate.py      # Recomendações
│   ├── Likes.py           # Histórico de likes
│   ├── Dislikes.py        # Histórico de dislikes
│   ├── Perfil.py          # Perfil do usuário
│   ├── Logout.py          # Desconexão
│   └── components/        # Componentes reutilizáveis
├── data/                  # Dados (raw, processed, embeddings)
├── tests/                 # Testes (pytest)
├── notebooks/             # Análise offline (Jupyter)
├── run.py                 # Script para iniciar tudo
├── requirements.txt       # Dependências
├── .gitignore            # Git ignore
└── README.md             # Este arquivo
```

## 🚀 Como Executar

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

- **Frontend Streamlit**: http://localhost:8501
- **Backend FastAPI**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com coverage
pytest --cov=app

# Teste específico
pytest tests/test_api.py -v
```

## 📊 Fluxo de Uso

1. **Login**: Usuário faz login/registro
2. **Slate**: Recebe 3-4 recomendações personalizadas
3. **Feedback**: Marca como like/dislike
4. **Modelo Atualiza**: Feedback é registrado e modelo se atualiza online
5. **Próximas Recomendações**: Baseadas em novo conhecimento

## 🤖 Algoritmo de Recomendação

- **Modelo**: LinUCB (Linear Upper Confidence Bound)
- **Contexto**: Features de usuário + features de item
- **Aprendizado**: Online com mini-batches
- **Exploração**: Balanceada com parâmetro alpha

## 🛠️ Desenvolvimento

### Direções Futuras

- [ ] Autenticação JWT
- [ ] Cache de recomendações
- [ ] Análise de A/B testing
- [ ] Dashboard de métricas
- [ ] Suporte a múltiplos modelos
- [ ] Deploy em cloud (Azure/AWS)

## 📚 Dependências Principais

- `fastapi` - Framework web
- `streamlit` - UI interativa
- `sqlalchemy` - ORM
- `mabwiser` - Bandit algoritmos
- `scikit-learn` - ML utilities
- `pytest` - Testes
- `pandas` - Processamento de dados

## 📝 Notas

- Banco de dados: SQLite (arquivo `data/database.db`)
- Embeddings: TF-IDF ou Sentence-Transformers (placeholder)
- Logs: `logs/app_*.log`
- Sessão: Streamlit session_state

## 📄 Licença

MVP educacional para demonstração de recomendação contextual.
