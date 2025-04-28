import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Ajusta sys.path automaticamente
project_root = os.getenv('PYTHONPATH')
if project_root and project_root not in sys.path:
    sys.path.append(project_root)

# Importações FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router

# Inicializa FastAPI
app = FastAPI(title="Buscador Multi Dados V2")

# 🚨 Adiciona Middleware CORS aqui
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Liberado para qualquer origem - podemos depois restringir se quiser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(router, prefix="/api/v1")

# Endpoint raiz
@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Buscador Multi Dados V2 🚀"}
