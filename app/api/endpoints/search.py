# backend/app/api/endpoints/search.py

from fastapi import APIRouter, HTTPException
from app.schemas.search import SearchOption1Request
from app.services.search_service import search_with_filters, search_in_all_tables
from app.core.config import engine
from app.core.logger import logger  # ✅ Logger centralizado

router = APIRouter()


@router.post("/search/option1", tags=["Busca"])
def search_option1(data: SearchOption1Request):
    """🔎 Busca por fonte específica com filtros."""
    field = data.field
    operator = data.operator
    term = data.term
    results = {}

    try:
        with engine.connect() as conn:
            for table in data.tables:
                try:
                    logger.info(f"[SEARCH_OPTION1] Consultando tabela: {table}")
                    res = search_with_filters(conn, table, field, operator, term)
                    if res:
                        results[table] = res
                except Exception as table_error:
                    logger.warning(f"[SEARCH_OPTION1] Falha na tabela {table}: {table_error}")

        logger.info(f"[SEARCH_OPTION1] Resultado final retornado: {len(results)} tabelas com dados.")
        return {"results": results or []}
    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro geral: {e}")
        raise HTTPException(status_code=500, detail="Erro interno na busca")


@router.post("/search/option2", tags=["Busca"])
def search_geral(data: dict):
    """🔎 Busca geral em todas as fontes (por CPF/CNPJ)."""
    try:
        number = data.get("number")
        if not number:
            raise ValueError("Campo 'number' é obrigatório.")

        with engine.connect() as conn:
            results = search_in_all_tables(conn, number)
            logger.info(f"[SEARCH_OPTION2] Busca geral completa. Fontes com dados: {len(results)}")
            return {"results": results or []}
    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro geral: {e}")
        raise HTTPException(status_code=500, detail="Erro na pesquisa geral")
