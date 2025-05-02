from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import search, metadata, export
import logging

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("buscador")

# Instância FastAPI
app = FastAPI(
    title="Buscador Multi Dados V3",
    version="1.0.0",
    description="API para buscas em múltiplas fontes de dados com filtros avançados e exportação."
)

# Configuração CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Rotas
app.include_router(search.router, prefix="/api/v1/search", tags=["Busca"])
app.include_router(metadata.router, prefix="/api/v1/tables", tags=["Metadados"])
app.include_router(export.router, prefix="/api/v1/export", tags=["Exportação"])

@app.get("/")
def root():
    logger.info("🌐 API Online")
    return {"message": "API Online"}
