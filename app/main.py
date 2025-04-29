from fastapi import FastAPI
from app.api.v1.endpoints import router
from app.core.config import settings

app = FastAPI(title="Buscador Multi Dados V2 🚀")

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Buscador Multi Dados V2"}
