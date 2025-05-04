import logging
from decimal import Decimal
from sqlalchemy.sql import text
from sqlalchemy.engine import Connection
from app.utils.metadata_utils import list_tables  # ✅ Uso correto, sem dependência circular

logger = logging.getLogger(__name__)

ALLOWED_OPERATORS = ['=', '!=', '>=', '<=', '>', '<']

# Campos mapeados (agregados) para termos unificados como 'CPF/CNPJ'
FIELD_MAPPINGS_TODAS = {
    'CPF/CNPJ': ['CPF', 'CNPJ', 'PN_CPF', 'PN_CNPJ', 'cpf', 'cnpj', 'CNPJ_EMPRESA'],
    'UF Geral': ['UF', 'PN_UF', 'ESTADO', 'UF_EMPRESA'],
    'CIDADE Geral': ['CIDADE', 'Cidade', 'MUNICIPIO_EMPRESA', 'OL_Municipio_ObjLig'],
    'Bairro Geral': ['BAIRRO', 'Distrito', 'OL_Bairro_ObjLig'],
    'CONSUMOS META': [
        'CONSUMO1', 'CONSUMO2', 'CONSUMO3', 'CONSUMO4', 'CONSUMO5',
        'CONSUMO6', 'CONSUMO7', 'CONSUMO8', 'CONSUMO9', 'CONSUMO10'
    ]
}


def validate_table_and_field(name: str) -> str:
    """Valida nomes de tabela/campo para prevenir SQL Injection."""
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
    """Executa busca simples em um campo."""
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


def search_multiple_fields(
    conn: Connection,
    table: str,
    fields: list[str],
    operator: str,
    term: str | int | float | Decimal
):
    """Tenta buscar em múltiplos campos na tabela, agregando resultados."""
    aggregated = []
    for field in fields:
        try:
            validate_table_and_field(field)
            logger.info(f"[SEARCH_MULTI] Tentando campo `{field}` em `{table}`")
            rows = search_with_filters(conn, table, field, operator, term)
            if rows:
                aggregated.extend(rows)
        except Exception as e:
            logger.warning(f"[SEARCH_MULTI] Falha em {table}.{field}: {e}")
    return aggregated


def search_in_all_tables(
    conn: Connection,
    number: str | int | Decimal
):
    """
    Executa busca geral em todos os campos equivalentes a CPF/CNPJ
    em todas as tabelas listadas pelo sistema.
    """
    results = {}

    try:
        tables_response = list_tables()
        tables = tables_response.get("tables", [])

        for table in tables:
            validate_table_and_field(table)
            logger.info(f"[SEARCH_OPTION2] Buscando em {table} com campos CPF/CNPJ")

            matches = search_multiple_fields(
                conn,
                table,
                FIELD_MAPPINGS_TODAS['CPF/CNPJ'],
                '=',
                number
            )

            if matches:
                results[table] = matches

        logger.info(f"[SEARCH_OPTION2] Resultado final retornado: {len(results)} tabelas com dados.")
        return results

    except Exception as e:
        logger.error(f"[SEARCH_OPTION2] Erro geral: {e}")
        raise
