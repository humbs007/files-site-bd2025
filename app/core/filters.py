# ✅ app/core/filters.py

from sqlalchemy.sql import and_, or_, func
from sqlalchemy.sql.sqltypes import String
from app.core.utils import normalize_term
from app.models.table_models import get_model_by_table
from app.core.logger import logger

def build_logic_clauses(table: str, filters: list[dict]) -> tuple:
    model = get_model_by_table(table)
    if not model:
        logger.warning(f"[FILTERS] Model não encontrado: {table}")
        return [], [f"[{table}] Model ausente"]

    logic_chain = []
    warnings = []

    for f in filters:
        sub_clauses = []
        term = normalize_term(f.get("term"))
        op = f.get("operator", "=")

        for field in f.get("fields", []):
            if not hasattr(model, field):
                msg = f"Campo '{field}' inexistente em {table}"
                logger.warning(f"[FILTERS] {msg}")
                warnings.append(msg)
                continue

            col = getattr(model, field)
            col_type = getattr(col, "type", None)
            is_str = isinstance(col_type, String)
            col_expr = func.lower(col) if is_str else col
            term_expr = term.lower() if is_str and isinstance(term, str) else term

            try:
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
                    if is_str and isinstance(term_expr, str):
                        clause = col_expr.like(f"%{term_expr}%")
                    else:
                        warnings.append(f"[{table}] LIKE inválido para campo '{field}'")
                        continue
                else:
                    warnings.append(f"[{table}] Operador inválido '{op}'")
                    continue

                sub_clauses.append(clause)
            except Exception as ex:
                warnings.append(f"[{table}] Erro no campo '{field}': {ex}")
                continue

        if sub_clauses:
            logic_op = and_ if f.get("logic", "AND") == "AND" else or_
            logic_chain.append(logic_op(*sub_clauses))

    return logic_chain, warnings
