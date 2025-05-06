# app/services/search_advanced.py

from sqlalchemy.engine import Connection
from app.core.database import engine
from app.core.query_builder import build_advanced_query
from app.core.validators import validate_table_and_field, validate_operator
from app.core.utils import normalize_term
import logging

logger = logging.getLogger(__name__)

def run_advanced_search(tables, filters):
    results = {}

    with engine.connect() as conn:
        for table in tables:
            try:
                validate_table_and_field(table)

                query, params = build_advanced_query(table, filters)
                logger.info(f"[ADVANCED] Query {table}: {query} | Params: {params}")

                rows = conn.execute(query, params).fetchall()
                if rows:
                    results[table] = [dict(row._mapping) for row in rows]

            except Exception as e:
                logger.error(f"[ADVANCED] Erro em {table}: {e}")

    return results
