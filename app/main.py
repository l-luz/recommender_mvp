"""
Entry point do FastAPI
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db.database import init_db, get_db
from .utils.config import FASTAPI_CONFIG
from .api import routes_slate, routes_feedback, routes_users

# Inicializar FastAPI
app = FastAPI(
    title=FASTAPI_CONFIG["title"],
    version=FASTAPI_CONFIG["version"]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar banco
@app.on_event("startup")
def startup_event():
    """Cria tabelas no startup"""
    init_db()
    print("✓ Database initialized")


# ==================== ROTAS ====================

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Recommender MVP API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.post("/slate")
def get_slate(user_id: int, n_items: int = 4, db: Session = Depends(get_db)):
    """Retorna recomendações (slate) para um usuário"""
    # TODO: Chamar routes_slate.get_slate
    return {"user_id": user_id, "recommendations": []}


@app.post("/feedback")
def register_feedback(feedback: dict, db: Session = Depends(get_db)):
    """Registra feedback (like/dislike)"""
    # TODO: Chamar routes_feedback.register_feedback
    return {"status": "ok"}


@app.post("/login")
def login(credentials: dict, db: Session = Depends(get_db)):
    """Autentica usuário"""
    # TODO: Chamar routes_users.login
    return {"user_id": 1, "token": "token"}


@app.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Retorna perfil do usuário"""
    # TODO: Chamar routes_users.get_profile
    return {"user_id": user_id, "preferences": {}}


@app.put("/profile/{user_id}")
def update_profile(user_id: int, profile: dict, db: Session = Depends(get_db)):
    """Atualiza perfil do usuário"""
    # TODO: Chamar routes_users.update_profile
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=FASTAPI_CONFIG["host"],
        port=FASTAPI_CONFIG["port"],
        reload=True
    )
