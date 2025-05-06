from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.search_service import advanced_search
from pydantic import BaseModel, Field
from typing import List, Literal

router = APIRouter()

class FilterInput(BaseModel):
    logic: Literal["AND", "OR"] = "AND"
    fields: List[str]
    operator: Literal["=", "!=", ">", "<", ">=", "<="]
    term: str | int | float

class AdvancedSearchRequest(BaseModel):
    tables: List[str]
    filters: List[FilterInput] = Field(..., min_items=1)

@router.post("/search/advanced")
async def search_advanced(
    request: AdvancedSearchRequest,
    db: AsyncSession = Depends(get_session)
):
    try:
        results = await advanced_search(db, request.tables, request.filters)
        return {"results": results}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no processamento da busca.")
