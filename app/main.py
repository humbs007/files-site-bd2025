from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import search, metadata, export
import logging

# Log global
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("buscador")

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 💥 ROTAS DEVERÃO ESTAR AQUI!
app.include_router(metadata.router, prefix="/api/v1/tables", tags=["Metadados"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Busca"])
app.include_router(export.router, prefix="/api/v1/export", tags=["Exportação"])

@app.get("/")
def root():
    logger.info("🌐 API Online")
    return {"message": "API Online"}
