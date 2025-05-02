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

        # Converte Decimal para string limpa (ex: CPF/CNPJ)
        if isinstance(term, Decimal):
            term = str(term)

        query = text(f"SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100")

        logger.info(f"[SEARCH_OPTION1] SQL: {query} | Termo: {term}")

        result = conn.execute(query, {"term": term})
        return [dict(row._mapping) for row in result.fetchall()]

    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro ao executar consulta: {e}")
        raise


def search_in_tables_by_term(
    conn: Connection,
    term: str | int | Decimal,
    table_fields: dict[str, list[str]]
):
    """Busca geral pelo termo em múltiplas tabelas/campos indexados."""
    results = {}

    try:
        for table, fields in table_fields.items():
            table = validate_table_and_field(table)
            matches = []

            for field in fields:
                field = validate_table_and_field(field)

                try:
                    query = text(f"SELECT * FROM `{table}` WHERE `{field}` = :number LIMIT 100")
                    logger.info(f"[SEARCH_OPTION2] SQL: {query} | Número: {term}")

                    result = conn.execute(query, {"number": term})
                    data = [dict(row._mapping) for row in result.fetchall()]

                    if data:
                        matches.extend(data)

                except Exception as field_error:
                    logger.warning(
                        f"[SEARCH_OPTION2] Falha ao consultar {table}.{field} | Erro: {field_error}"
                    )

            if matches:
                results[table] = matches

        return results

    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro geral: {e}")
        raise
