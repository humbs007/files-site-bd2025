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
from app.core.filters import build_logic_clauses  # ✅ Correto agora

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
    for field in fields:
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
        tables, fields = get_tables_and_unified_fields()
        normalized = normalize_term(number)

        for table in tables:
            validate_table_and_field(table)
            logger.info(f"[SEARCH_OPTION2] {table} com campos {fields}")
            matches = search_multiple_fields(conn, table, fields, '=', normalized)
            if matches:
                results[table] = matches

        return results
    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro na busca geral: {e}")
        raise


# 🧠 Cache com fallback seguro baseado em UNIFIED_FIELDS reais
def get_tables_and_unified_fields() -> Tuple[List[str], List[str]]:
    now = time.time()
    if "timestamp" in _table_cache and (now - _table_cache["timestamp"] < _cache_ttl):
        logger.debug("[CACHE] Usando cache de tabelas/campos")
        return _table_cache["tables"], _table_cache["unified_fields"]

    logger.debug("[CACHE] Recalculando DB_SCHEMA + fallback")
    try:
        tables = list(DB_SCHEMA.get("tabelas", {}).keys())
        unified = UNIFIED_FIELDS.get("CPF/CNPJ", [])
        if not unified:
            raise ValueError("Sem campos unificados em UNIFIED_FIELDS")

        _table_cache.update({
            "timestamp": now,
            "tables": tables,
            "unified_fields": unified
        })
        return tables, unified

    except Exception as e:
        logger.warning(f"[SCHEMA_FALLBACK] Falha ao ler UNIFIED_FIELDS ou DB_SCHEMA: {e}")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        fields = set()
        for table in tables:
            try:
                indexes = inspector.get_indexes(table)
                for idx in indexes:
                    fields.update(idx.get("column_names", []))
                pk = inspector.get_pk_constraint(table).get("constrained_columns", [])
                fields.update(pk)
            except Exception as e2:
                logger.warning(f"[SCHEMA_FALLBACK] Falha inspecionando {table}: {e2}")

        fields_sorted = sorted(fields)
        _table_cache.update({
            "timestamp": now,
            "tables": tables,
            "unified_fields": fields_sorted
        })
        return tables, fields_sorted


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

            logic_chain, warnings = build_logic_clauses(table, filters)
            if warnings:
                for w in warnings:
                    logger.warning(f"[ADV_SEARCH_WARN] {w}")

            if not logic_chain:
                logger.info(f"[ADV_SEARCH] Nenhum filtro aplicável para {table}")
                continue

            full_query = select(model).where(*logic_chain).limit(100)
            result = db.execute(full_query)
            data = result.scalars().all()

            if data:
                results[table] = [row.__dict__ for row in data]

        except Exception as e:
            logger.exception(f"[ADV_SEARCH] Erro inesperado em tabela {table}: {e}")

    return results
