# ✅ backend/app/schemas/filters.py

from pydantic import BaseModel
from typing import List, Optional

class FilterItem(BaseModel):
    logic: Optional[str] = None  # "AND" ou "OR"
    fields: List[str]            # Lista de campos reais mapeados
    operator: str                # '=', '!=', 'like', etc
    term: str                    # Termo de busca

class SearchAdvancedRequest(BaseModel):
    tables: List[str]
    filters: List[FilterItem]
