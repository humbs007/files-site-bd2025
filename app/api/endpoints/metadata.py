from fastapi import APIRouter
from app.db.queries import get_tables_and_indexes

router = APIRouter()

@router.get("/")
def get_metadata():
    return {"tables": get_tables_and_indexes()}
