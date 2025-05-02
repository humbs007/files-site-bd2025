# backend/app/services/search_service.py

import logging
from sqlalchemy.sql import text
from decimal import Decimal

logger = logging.getLogger(__name__)

def search_with_filters(conn, table: str, field: str, operator: str, term: str):
    try:
        # ✅ Operadores permitidos
        if operator not in ['=', '!=', '>=', '<=', '>', '<']:
            raise ValueError(f"Operador inválido: {operator}")

        # 🔒 Sanitização do nome do campo e tabela
        if not field.replace("_", "").isalnum() or not table.replace("_", "").isalnum():
            raise ValueError("Nome de campo ou tabela inválido")

        # 📢 Logging para auditoria e debug
        logger.info(f"[SEARCH_OPTION1] SQL: SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100 | Termo: {term}")

        # 🔄 Normalização do termo (evita erro com Decimal)
        if isinstance(term, Decimal):
            term = str(term)

        # 🛡️ Query segura
        query = text(f"SELECT * FROM `{table}` WHERE `{field}` {operator} :term LIMIT 100")
        result = conn.execute(query, {"term": term})

        # ✅ Resultado convertido para lista de dicionários
        return [dict(row._mapping) for row in result.fetchall()]

    except Exception as e:
        logger.error(f"[SEARCH_OPTION1] Erro ao executar consulta: {e}")
        raise
