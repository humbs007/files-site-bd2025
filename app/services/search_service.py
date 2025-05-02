import logging
from sqlalchemy.sql import text
from decimal import Decimal

logger = logging.getLogger(__name__)

# Validação simples para evitar SQL Injection
def is_valid_identifier(name: str) -> bool:
    return name.replace("_", "").isalnum()

# 🔎 Função principal de busca com filtros
def search_with_filters(conn, table: str, field: str, operator: str, term):
    try:
        if operator not in ['=', '!=', '>=', '<=', '>', '<']:
            raise ValueError(f"Operador inválido: {operator}")

        if not (is_valid_identifier(table) and is_valid_identifier(field)):
            raise ValueError("Nome de tabela ou campo inválido")

        # Sanitiza o valor do termo
        if isinstance(term, Decimal):
            term = str(term)

        logger.info(f"[SEARCH_OPTION1] SQL: SELECT * FROM {table} WHERE {field} {operator} :term LIMIT 100 | Termo: {term}")

        query = text(f"SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100")
        result = conn.execute(query, {"term": term})
        return [dict(row._mapping) for row in result.fetchall()]

    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro ao executar consulta: {e}")
        raise


# 🔁 Busca geral: percorre múltiplas tabelas e tenta encontrar correspondências por CPF/CNPJ
def search_in_all_tables(conn, number):
    from sqlalchemy import inspect
    inspector = inspect(conn)
    all_tables = inspector.get_table_names()

    index_fields = {
        "table_enel": ["PN_CPF", "PN_CNPJ"],
        "table_meta": ["CPF"],
        "table_credlink": ["CPF"]
    }

    results = {}

    for table in all_tables:
        fields = index_fields.get(table, [])
        for field in fields:
            try:
                logger.info(f"[SEARCH_OPTION2] SQL: SELECT * FROM {table} WHERE {field} = :number LIMIT 100 | Número: {number}")
                query = text(f"SELECT * FROM `{table}` WHERE `{field}` = :number LIMIT 100")
                result = conn.execute(query, {"number": str(number)})
                rows = [dict(row._mapping) for row in result.fetchall()]
                if rows:
                    if table not in results:
                        results[table] = []
                    results[table].extend(rows)
            except Exception as e:
                logger.warning(f"[SEARCH_OPTION2] Falha ao consultar {table}.{field} | Erro: {e}")

    return results
