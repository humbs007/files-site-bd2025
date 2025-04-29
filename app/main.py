from fastapi import FastAPI
from app.api.endpoints import metadata, search, export

app = FastAPI(title="Buscador Multi Dados V3 - Backend")

app.include_router(metadata.router, prefix="/metadata", tags=["Metadata"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(export.router, prefix="/export", tags=["Export"])
