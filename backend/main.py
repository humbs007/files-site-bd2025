import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Ajusta sys.path automaticamente
project_root = os.getenv('PYTHONPATH')
if project_root and project_root not in sys.path:
    sys.path.append(project_root)

# Agora sim, importa normalmente
from fastapi import FastAPI
from app.api.v1.endpoints import router

app = FastAPI(title="Buscador Multi Dados V2")

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Buscador Multi Dados V2 🚀"}
