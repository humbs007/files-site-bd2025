from fastapi import APIRouter, HTTPException
from app.schemas.search import SearchOption1Request
from app.core.config import engine
from app.services.search_service import search_with_filters
from sqlalchemy import text
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/option1")
def search_option1(data: SearchOption1Request):
    field = data.field
    operator = data.operator
    term = data.term
    results = {}

    try:
        with engine.connect() as conn:
            for table in data.tables:
                try:
                    logger.info(f"[SEARCH_OPTION1] Consultando tabela {table}")
                    table_results = search_with_filters(conn, table, field, operator, term)
                    if table_results:
                        results[table] = table_results
                except Exception as table_error:
                    logger.warning(f"[SEARCH_OPTION1] Erro ao consultar {table}: {table_error}")

        if not results:
            return {"results": []}

        return {"results": results}

    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro geral: {e}")
        raise HTTPException(status_code=500, detail="Erro interno na busca")


@router.post("/option2")
def search_option2(payload: dict):
    number = payload.get("number")
    results = {}

    if not number:
        raise HTTPException(status_code=400, detail="Parâmetro 'number' obrigatório.")

    try:
        with engine.connect() as conn:
            tables = ["table_enel", "table_meta", "table_credlink"]
            field_candidates = ["PN_CPF", "PN_CNPJ", "CPF", "CNPJ"]

            for table in tables:
                for field in field_candidates:
                    try:
                        query = text(f"SELECT * FROM `{table}` WHERE `{field}` = :number LIMIT 100")
                        logger.info(f"[SEARCH_OPTION2] SQL: {query} | Número: {number}")
                        result = conn.execute(query, {"number": number})
                        rows = result.fetchall()
                        if rows:
                            results[table] = [dict(row._mapping) for row in rows]
                            break  # parar após o primeiro campo que der match
                    except Exception as query_error:
                        logger.warning(f"[SEARCH_OPTION2] Falha ao consultar {table}.{field} | Erro: {query_error}")
                        continue

        if not results:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado.")

        return {"results": results}

    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro geral: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")
