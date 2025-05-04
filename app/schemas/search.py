# backend/app/schemas/search.py

from pydantic import BaseModel
from typing import List, Union

class SearchOption1Request(BaseModel):
    tables: List[str]
    field: str
    operator: str
    term: Union[str, int, float]
