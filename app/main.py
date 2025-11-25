"""
Entry point do FastAPI
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core import rl_runtime as rl
from .db.database import get_db
from .utils.config import FASTAPI_CONFIG
from .api import routes_slate, routes_feedback, routes_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Função de Lifespan para inicializar o runtime do RL no startup.
    """
    db = next(get_db())
    rl.init_runtime(db)
    yield


# ==================== FastAPI ====================
app = FastAPI(
    title=FASTAPI_CONFIG["title"], version=FASTAPI_CONFIG["version"], lifespan=lifespan
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ==================== ROUTES ====================
app.include_router(routes_feedback.router)
app.include_router(routes_users.router)
app.include_router(routes_slate.router)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Recommender MVP API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=FASTAPI_CONFIG["host"],
        port=FASTAPI_CONFIG["port"],
        reload=True,
    )
