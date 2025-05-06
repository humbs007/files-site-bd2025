# ✅ backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import metadata, search, export, advanced
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("buscador")

app = FastAPI(
    title="Buscador Multidados V3",
    description="Sistema de busca cruzada entre bases ENEL, META e CREDLINK",
    version="1.0.0"
)

# 🌐 Permite conexão com frontend local
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 🔌 Prefixo comum da API
api_prefix = "/api/v1"

# 🚀 Rotas registradas
app.include_router(metadata.router, prefix=f"{api_prefix}/tables", tags=["Metadados"])
app.include_router(search.router, prefix=f"{api_prefix}/search", tags=["Busca"])
app.include_router(export.router, prefix=f"{api_prefix}/export", tags=["Exportação"])
app.include_router(advanced.router, prefix=f"{api_prefix}/search", tags=["Busca Avançada"])  # ✅ NOVO

@app.get("/")
def root():
    logger.info("🌐 API Online")
    return {"message": "API Online"}
