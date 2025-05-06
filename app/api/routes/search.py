from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.services.search_advanced import run_advanced_search

router = APIRouter()

class FilterItem(BaseModel):
    logic: str | None
    fields: list[str]
    operator: str
    term: str

class SearchAdvancedRequest(BaseModel):
    tables: list[str]
    filters: list[FilterItem]

@router.post("/api/v1/search/advanced")
def advanced_search(payload: SearchAdvancedRequest, request: Request):
    results = run_advanced_search(payload.tables, payload.filters)
    return {"results": results}
