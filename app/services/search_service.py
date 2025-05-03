# backend/app/services/search_service.py

import logging
from decimal import Decimal
from sqlalchemy.sql import text
from sqlalchemy.engine import Connection

logger = logging.getLogger(__name__)

ALLOWED_OPERATORS = ['=', '!=', '>=', '<=', '>', '<']

def validate_table_and_field(name: str) -> str:
    """Valida nome de tabela/campo para prevenir SQL Injection."""
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
    """Executa busca por campo/index com operador e termo definido."""
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
        raise


def search_in_all_tables(
    conn: Connection,
    number: str | int | Decimal
):
    """
    Executa busca geral em todas as tabelas conhecidas, nos campos comuns.
    """
    results = {}
    try:
        # Campos comuns manualmente definidos
        common_fields = ['CPF', 'PN_CPF', 'CNPJ', 'PN_CNPJ']
        from app.api.endpoints.metadata import list_tables
        tables_response = list_tables()
        tables = tables_response.get("tables", [])

        for table in tables:
            validate_table_and_field(table)
            matches = []

            for field in common_fields:
                try:
                    validate_table_and_field(field)
                    query = text(f"SELECT * FROM `{table}` WHERE `{field}` = :number LIMIT 100")
                    logger.info(f"[SEARCH_OPTION2] SQL: {query} | Número: {number}")

                    result = conn.execute(query, {"number": number})
                    data = [dict(row._mapping) for row in result.fetchall()]
                    if data:
                        matches.extend(data)
                except Exception as fe:
                    logger.warning(f"[SEARCH_OPTION2] Erro em {table}.{field}: {fe}")

            if matches:
                results[table] = matches

        return results
    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro geral: {e}")
        raise
