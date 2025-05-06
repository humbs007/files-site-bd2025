import logging
import time
from decimal import Decimal
from typing import List, Tuple

from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from app.core.database import engine
from app.core.db_schema_config import DB_SCHEMA, UNIFIED_FIELDS
from app.core.query_builder import build_query
from app.core.validators import validate_table_and_field, validate_operator
from app.core.utils import normalize_term
from app.models.table_models import get_model_by_table
from app.core.filters import build_logic_clauses

logger = logging.getLogger(__name__)
_table_cache = {}
_cache_ttl = 600  # segundos


# 🎯 Busca simples por campo/valor
def search_with_filters(
    conn: Session,
    table: str,
    field: str,
    operator: str,
    term: str | int | float | Decimal
):
    try:
        validate_table_and_field(table)
        validate_table_and_field(field)
        validate_operator(operator)

        query = build_query(table, field, operator)
        normalized = normalize_term(term)
        logger.info(f"[SEARCH_OPTION1] SQL: {query} | Termo: {normalized}")

        result = conn.execute(query, {"term": normalized})
        return [dict(row._mapping) for row in result.fetchall()]
    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro na consulta: {e}")
        return []


# 🔁 Busca em múltiplos campos, sem duplicatas
def search_multiple_fields(
    conn: Session,
    table: str,
    fields: List[str],
    operator: str,
    term: str | int | float | Decimal
):
    seen = {}
    model = get_model_by_table(table)
    if not model:
        logger.warning(f"[SEARCH_MULTI] Model ausente para {table}")
        return []

    valid_fields = [f for f in fields if hasattr(model, f)]

    for field in valid_fields:
        try:
            rows = search_with_filters(conn, table, field, operator, term)
            for row in rows:
                key = str(row.get("id") or hash(frozenset(row.items())))
                seen[key] = row
        except Exception as e:
            logger.warning(f"[SEARCH_MULTI] Falha em {table}.{field}: {e}")
    return list(seen.values())


# 🔍 Busca geral com campos unificados
def search_in_all_tables(
    conn: Session,
    number: str | int | Decimal
):
    results = {}
    try:
        tables, fields_by_table = get_tables_and_unified_fields()
        normalized = normalize_term(number)

        for table in tables:
            validate_table_and_field(table)
            model_fields = fields_by_table.get(table, [])
            if not model_fields:
                continue

            logger.info(f"[SEARCH_OPTION2] {table} com campos {model_fields}")
            matches = search_multiple_fields(conn, table, model_fields, '=', normalized)
            if matches:
                results[table] = matches

        return results
    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro na busca geral: {e}")
        raise


# 🧠 Cache com fallback seguro baseado em UNIFIED_FIELDS reais
def get_tables_and_unified_fields() -> Tuple[List[str], dict]:
    now = time.time()
    if "timestamp" in _table_cache and (now - _table_cache["timestamp"] < _cache_ttl):
        logger.debug("[CACHE] Usando cache de tabelas/campos")
        return _table_cache["tables"], _table_cache["unified_fields"]

    logger.debug("[CACHE] Recalculando DB_SCHEMA + fallback")
    try:
        inspector = inspect(engine)
        all_tables = inspector.get_table_names()
        filtered_tables = []
        unified_by_table = {}

        for table in all_tables:
            try:
                columns = {col["name"] for col in inspector.get_columns(table)}
                valid_fields = []
                for group in UNIFIED_FIELDS.values():
                    valid_fields.extend([f for f in group if f in columns])
                if valid_fields:
                    unified_by_table[table] = sorted(set(valid_fields))
                    filtered_tables.append(table)
            except Exception as e:
                logger.warning(f"[CACHE] Falha ao processar tabela {table}: {e}")

        _table_cache.update({
            "timestamp": now,
            "tables": filtered_tables,
            "unified_fields": unified_by_table
        })
        return filtered_tables, unified_by_table

    except Exception as e:
        logger.error(f"[CACHE] Falha geral ao obter tabelas/unificados: {e}")
        return [], {}


# 🚀 Busca avançada com múltiplos filtros (via filters.py)
def advanced_search(
    db: Session,
    tables: list[str],
    filters: list[dict]
) -> dict:
    results = {}

    for table in tables:
        try:
            validate_table_and_field(table)
            model = get_model_by_table(table)
            if not model:
                logger.warning(f"[ADV_SEARCH] Model não encontrado para {table}")
                continue

            # ⚠️ Remove campos inexistentes antes de gerar cláusulas
            safe_filters = []
            for f in filters:
                real_fields = [field for field in f["fields"] if hasattr(model, field)]
                if real_fields:
                    safe_filters.append({**f, "fields": real_fields})
                else:
                    logger.warning(f"[FILTERS] Nenhum campo válido em {f['fields']} para {table}")

            if not safe_filters:
                logger.info(f"[ADV_SEARCH] Nenhum filtro aplicável para {table}")
                continue

            logic_chain, warnings = build_logic_clauses(table, safe_filters)
            if warnings:
                for w in warnings:
                    logger.warning(f"[ADV_SEARCH_WARN] {w}")

            if not logic_chain:
                continue

            full_query = select(model).where(*logic_chain).limit(100)
            result = db.execute(full_query)
            data = result.scalars().all()

            if data:
                results[table] = [row.__dict__ for row in data]

        except Exception as e:
            logger.exception(f"[ADV_SEARCH] Erro inesperado em tabela {table}: {e}")

    return results
