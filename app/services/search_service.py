import logging
from decimal import Decimal
from sqlalchemy import inspect
from sqlalchemy.sql import text
from sqlalchemy.engine import Connection
from app.core.database import engine  # ✅ CONEXÃO PRINCIPAL
from app.core.db_schema_config import DB_SCHEMA  # 🔎 Para labels e mapeamento unificado

logger = logging.getLogger(__name__)

ALLOWED_OPERATORS = ['=', '!=', '>=', '<=', '>', '<']


def validate_table_and_field(name: str) -> str:
    """✅ Valida nomes para evitar SQL Injection."""
    if not name.replace("_", "").isalnum():
        raise ValueError(f"Nome inválido detectado: {name}")
    return name


def search_with_filters(
    conn: Connection,
    table: str,
    field: str,
    operator: str,
    term: str | int | float | Decimal
):
    """🎯 Executa busca simples por campo único."""
    try:
        validate_table_and_field(table)
        validate_table_and_field(field)

        if operator not in ALLOWED_OPERATORS:
            raise ValueError(f"Operador inválido: {operator}")

        if isinstance(term, Decimal):
            term = str(term)

        query = text(f"SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100")
        logger.info(f"[SEARCH_OPTION1] SQL: {query} | Termo: {term}")

        result = conn.execute(query, {"term": term})
        return [dict(row._mapping) for row in result.fetchall()]

    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro ao executar consulta: {e}")
        return []


def search_multiple_fields(
    conn: Connection,
    table: str,
    fields: list[str],
    operator: str,
    term: str | int | float | Decimal
):
    """🔁 Executa busca tentando todos os campos fornecidos, sem duplicar resultados."""
    seen = {}
    for field in fields:
        try:
            validate_table_and_field(field)
            logger.info(f"[SEARCH_MULTI] Tentando campo `{field}` em `{table}`")
            rows = search_with_filters(conn, table, field, operator, term)

            for row in rows:
                row_key = str(row.get("id") or hash(frozenset(row.items())))
                seen[row_key] = row

        except Exception as e:
            logger.warning(f"[SEARCH_MULTI] Falha em {table}.{field}: {e}")

    return list(seen.values())


def get_tables_and_unified_fields():
    """
    🧠 Recupera tabelas + campos unificados da config.
    Se falhar, tenta dinamicamente com SQLAlchemy Inspector.
    """
    try:
        tables = list(DB_SCHEMA.get("tabelas", {}).keys())
        unified_fields = DB_SCHEMA.get("unificados", {}).get("CPF/CNPJ", [])
        if not unified_fields:
            raise ValueError("Nenhum campo unificado encontrado.")
        return tables, unified_fields
    except Exception as e:
        logger.warning(f"[SCHEMA_FALLBACK] DB_SCHEMA incompleto, usando fallback via inspector: {e}")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        fields_set = set()

        for table in tables:
            try:
                pk_cols = inspector.get_pk_constraint(table).get("constrained_columns", [])
                indexes = inspector.get_indexes(table)
                for idx in indexes:
                    fields_set.update(idx.get("column_names", []))
                fields_set.update(pk_cols)
            except Exception as e2:
                logger.warning(f"[SCHEMA_FALLBACK] Falha ao inspecionar {table}: {e2}")

        return tables, sorted(fields_set)


def search_in_all_tables(
    conn: Connection,
    number: str | int | Decimal
):
    """🔍 Busca geral em todas as tabelas com campos unificados."""
    results = {}
    try:
        tables, campos_unificados = get_tables_and_unified_fields()

        for table in tables:
            validate_table_and_field(table)
            logger.info(f"[SEARCH_OPTION2] Buscando em {table} com campos: {campos_unificados}")
            matches = search_multiple_fields(conn, table, campos_unificados, '=', number)
            if matches:
                results[table] = matches

        return results

    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro geral: {e}")
        raise
