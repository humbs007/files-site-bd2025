# app/api/endpoints/advanced.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from app.services.search_service import advanced_search
from app.core.database import get_db

router = APIRouter()

class FilterItem(BaseModel):
    logic: Optional[str] = None  # "AND", "OR"
    fields: List[str]
    operator: str
    term: str

class SearchAdvancedRequest(BaseModel):
    tables: List[str]
    filters: List[FilterItem]

@router.post("/advanced")
def advanced_search_endpoint(
    payload: SearchAdvancedRequest,
    db: Session = Depends(get_db)
):
    """
    🔍 Executa busca com múltiplos filtros e lógica booleana.
    Compatível com valores insensíveis a caixa (UPPER/lower).
    """
    results = advanced_search(
        db=db,
        tables=payload.tables,
        filters=[f.dict() for f in payload.filters]
    )
    return {"results": results}
