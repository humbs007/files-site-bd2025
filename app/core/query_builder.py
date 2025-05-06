from sqlalchemy.sql import text
from app.core.validators import validate_table_and_field, validate_operator


def build_query(table: str, field: str, operator: str):
    """
    🧱 Monta query simples com segurança contra SQL injection.
    """
    validate_table_and_field(table)
    validate_table_and_field(field)
    validate_operator(operator)

    return text(f"SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100")


def build_advanced_query(table: str, filters: list[dict]):
    """
    🔁 Constrói query avançada com múltiplos filtros e lógica booleana.
    """
    clauses = []
    params = {}

    for idx, f in enumerate(filters):
        logic = f.get("logic")
        fields = f["fields"]
        operator = f["operator"]
        term = f["term"]

        validate_operator(operator)

        sub_conditions = [
            f"`{validate_table_and_field(field)}` {operator} :term{idx}" for field in fields
        ]
        group_clause = " OR ".join(sub_conditions)
        clause = f"{logic} ({group_clause})" if logic else f"({group_clause})"
        clauses.append(clause)

        params[f"term{idx}"] = term

    where_clause = " ".join(clauses)
    sql = f"SELECT * FROM `{table}` WHERE {where_clause} LIMIT 100"
    return text(sql), params
