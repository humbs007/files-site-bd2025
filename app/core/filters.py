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
        op = (f.get("operator") or "=").upper()

        for field in f.get("fields", []):
            if not hasattr(model, field):
                msg = f"Campo '{field}' inexistente em {table}"
                logger.warning(f"[FILTERS] {msg}")
                warnings.append(msg)
                continue

            col = getattr(model, field)
            col_type = getattr(col, "type", None)
            is_str = isinstance(col_type, String)
            use_lower = is_str and isinstance(term, str) and op in ["=", "LIKE"]

            col_expr = func.lower(col) if use_lower else col
            term_expr = term.lower() if use_lower else term

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
                elif op == "LIKE":
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
                logger.exception(f"[FILTERS] Erro processando cláusula {field} em {table}")
                warnings.append(f"[{table}] Erro no campo '{field}': {ex}")
                continue

        if sub_clauses:
            logic_raw = f.get("logic")
            logic = (logic_raw or "AND").upper()
            logic_op = and_ if logic == "AND" else or_
            logic_chain.append(logic_op(*sub_clauses))

    return logic_chain, warnings