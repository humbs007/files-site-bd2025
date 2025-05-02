from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import search, metadata, export
import logging

# 🔧 Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("buscador")

# 🚀 Instância principal FastAPI
app = FastAPI(
    title="Buscador Multi Dados V3",
    version="1.0.0",
    description="API para buscas em múltiplas tabelas e campos com filtros avançados."
)

# 🌐 CORS - permitir frontend acessar backend localmente
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# 🧱 Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Registro dos módulos de rota com prefixo unificado
api_prefix = "/api/v1"
app.include_router(metadata.router, prefix=api_prefix)
app.include_router(search.router, prefix=api_prefix)
app.include_router(export.router, prefix=api_prefix)

# 🧪 Endpoint base (saúde)
@app.get("/")
def root():
    logger.info("🌐 API Online")
    return {"message": "API Online"}
