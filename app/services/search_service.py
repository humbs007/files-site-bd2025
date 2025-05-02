from decimal import Decimal
from sqlalchemy.sql import text
from sqlalchemy.engine import Connection
from app.core.logger import logger  # 🔁 Importa logger centralizado

ALLOWED_OPERATORS = ['=', '!=', '>=', '<=', '>', '<']

def validate_table_and_field(name: str) -> str:
    """🔐 Valida nome de tabela/campo para prevenir SQL Injection."""
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
    """🔎 Busca específica com filtros."""
    try:
        table = validate_table_and_field(table)
        field = validate_table_and_field(field)

        if operator not in ALLOWED_OPERATORS:
            raise ValueError(f"Operador inválido: {operator}")

        if isinstance(term, Decimal):
            term = str(term)

        query = text(f"SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100")
        logger.info(f"[SEARCH_OPTION1] SQL: SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100 | Termo: {term}")

        result = conn.execute(query, {"term": term})
        data = [dict(row._mapping) for row in result.fetchall()]

        logger.info(f"[SEARCH_OPTION1] Registros retornados: {len(data)}")
        return data

    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro ao buscar em {table}.{field} com operador '{operator}' e termo '{term}': {e}")
        raise

def search_in_tables_by_term(
    conn: Connection,
    term: str | int | Decimal,
    table_fields: dict[str, list[str]]
):
    """🌐 Busca geral em múltiplas tabelas e campos indexados."""
    results = {}

    try:
        for table, fields in table_fields.items():
            table = validate_table_and_field(table)
            matches = []

            for field in fields:
                field = validate_table_and_field(field)

                try:
                    query = text(f"SELECT * FROM `{table}` WHERE `{field}` = :number LIMIT 100")
                    logger.info(f"[SEARCH_OPTION2] SQL: SELECT * FROM `{table}` WHERE `{field}` = :number LIMIT 100 | Número: {term}")

                    result = conn.execute(query, {"number": term})
                    data = [dict(row._mapping) for row in result.fetchall()]

                    if data:
                        logger.info(f"[SEARCH_OPTION2] {len(data)} registros encontrados em {table}.{field}")
                        matches.extend(data)

                except Exception as field_error:
                    logger.warning(f"[SEARCH_OPTION2] Falha ao consultar {table}.{field}: {field_error}")

            if matches:
                results[table] = matches

        return results

    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro geral na busca por termo '{term}': {e}")
        raise
