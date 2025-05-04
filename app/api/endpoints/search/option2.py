# backend/app/api/endpoints/search/option2.py

from fastapi import APIRouter, Request
from app.core.database import engine
from app.services.search_service import search_in_all_tables

router = APIRouter()

@router.post("", tags=["Busca Geral"])
async def search_all(request: Request):
    payload = await request.json()
    number = payload.get("number")

    with engine.connect() as conn:
        results = search_in_all_tables(conn, number)

    return {"results": results}
