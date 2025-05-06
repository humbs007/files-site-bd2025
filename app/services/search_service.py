import logging
import time
from decimal import Decimal
from typing import List, Tuple

from sqlalchemy import inspect, select, and_, or_, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import String  # 👈 necessário para verificação de tipo

from app.core.database import engine
from app.core.db_schema_config import DB_SCHEMA, UNIFIED_FIELDS
from app.core.query_builder import build_query
from app.core.validators import validate_table_and_field, validate_operator
from app.core.utils import normalize_term
from app.models.table_models import get_model_by_table

logger = logging.getLogger(__name__)
_table_cache = {}
_cache_ttl = 600  # segundos


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


def advanced_search(
    db: Session,
    tables: list[str],
    filters: list[dict]
) -> dict:
    results = {}

    for table in tables:
        validate_table_and_field(table)
        model = get_model_by_table(table)
        if not model:
            continue

        logic_chain = []
        for f in filters:
            sub_clauses = []
            for field in f["fields"]:
                validate_table_and_field(field)
                col = getattr(model, field, None)
                if col is None:
                    continue

                term = normalize_term(f["term"])
                op = f["operator"]

                if isinstance(col.type, String):
                    col_expr = func.lower(col)
                    term_expr = term.lower() if isinstance(term, str) else term
                else:
                    col_expr = col
                    term_expr = term

                if op == "=":
                    clause = col_expr == term_expr
                elif op == "!=":
                    clause = col_expr != term_expr
                elif op == ">":
                    clause = col > term
                elif op == "<":
                    clause = col < term
                elif op == ">=":
                    clause = col >= term
                elif op == "<=":
                    clause = col <= term
                elif op.lower() == "like":
                    if isinstance(col.type, String) and isinstance(term_expr, str):
                        clause = col_expr.like(f"%{term_expr}%")
                    else:
                        continue
                else:
                    raise ValueError(f"Operador inválido: {op}")

                sub_clauses.append(clause)

            if not sub_clauses:
                continue

            logic_op = and_ if f.get("logic", "AND") == "AND" else or_
            logic_chain.append(logic_op(*sub_clauses))

        if not logic_chain:
            continue

        full_query = select(model).where(and_(*logic_chain)).limit(100)
        result = db.execute(full_query)
        data = result.scalars().all()

        if data:
            results[table] = [row.__dict__ for row in data]

    return results
