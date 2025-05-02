# backend/app/schemas/search.py

from pydantic import BaseModel, Field
from typing import List

class SearchOption1Request(BaseModel):
    tables: List[str] = Field(..., example=["table_enel", "table_meta", "table_credlink"])
    field: str = Field(..., example="PN_CPF")
    operator: str = Field(..., example="=")
    term: str = Field(..., example="28545840829")
