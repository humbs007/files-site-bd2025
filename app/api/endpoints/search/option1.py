# backend/app/api/endpoints/search/option1.py

from fastapi import APIRouter, Request
from app.core.database import engine
from app.services.search_service import search_multiple_fields
from sqlalchemy import create_engine

router = APIRouter()

@router.post("", tags=["Busca Fonte"])
async def search_from_source(request: Request):
    payload = await request.json()
    tables = payload.get("tables", [])
    fields = payload.get("fields", [])
    operator = payload.get("operator", "=")
    term = payload.get("term", "")

    results = {}
    with engine.connect() as conn:
        for table in tables:
            rows = search_multiple_fields(conn, table, fields, operator, term)
            if rows:
                results[table] = rows

    return {"results": results}
