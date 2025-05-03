# ✅ backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import search, metadata, export
import logging

# 🔐 Logging centralizado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("buscador")

# 🎯 Instância da API com nome e descrição
app = FastAPI(
    title="Buscador Multidados V3",
    description="Sistema de busca cruzada entre bases ENEL, META e CREDLINK",
    version="1.0.0"
)

# 🌐 CORS Config
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 🧭 Prefixo versionado
api_prefix = "/api/v1"

# 🔌 Registro de rotas por módulo
app.include_router(metadata.router, prefix=f"{api_prefix}/tables", tags=["Metadados"])
app.include_router(search.router, prefix=f"{api_prefix}/search", tags=["Busca"])
app.include_router(export.router, prefix=f"{api_prefix}/export", tags=["Exportação"])

# 🌐 Rota raiz
@app.get("/")
def root():
    logger.info("🌐 API Online")
    return {"message": "API Online"}
