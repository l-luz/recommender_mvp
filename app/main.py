"""
Entry point do FastAPI
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db.database import init_db
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

# Incluir routers
app.include_router(routes_feedback.router)
app.include_router(routes_users.router)
app.include_router(routes_slate.router)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Recommender MVP API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=FASTAPI_CONFIG["host"],
        port=FASTAPI_CONFIG["port"],
        reload=True
    )
