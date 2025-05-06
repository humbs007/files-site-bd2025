# ✅ app/api/endpoints/advanced.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.search_service import advanced_search
from app.core.database import get_db
from app.schemas.filters import SearchAdvancedRequest  # ✅ import refatorado
from app.core.logger import logger

router = APIRouter()


@router.post("/advanced")
def advanced_search_endpoint(
    payload: SearchAdvancedRequest,
    db: Session = Depends(get_db)
):
    """
    🔍 Executa busca com múltiplos filtros e lógica booleana.
    Compatível com valores insensíveis a caixa (UPPER/lower).
    """
    try:
        results = advanced_search(
            db=db,
            tables=payload.tables,
            filters=[f.dict() for f in payload.filters]
        )
        return {"results": results}
    except Exception as e:
        logger.error(f"[ADVANCED_ENDPOINT] Erro na busca: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao processar busca avançada.")
