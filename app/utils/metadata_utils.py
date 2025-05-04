# backend/app/utils/metadata_utils.py

from sqlalchemy.engine import Connection
from app.core.config import engine
from app.core.logger import logger

TABLES = [
    "table_cemig", "table_credlink", "table_enel",
    "table_meta", "table_plano_saude", "table_vidatoda"
]

def list_tables():
    """Retorna as tabelas disponíveis."""
    try:
        logger.info("[METADATA_UTILS] Tabelas carregadas com sucesso.")
        return {"tables": TABLES}
    except Exception as e:
        logger.error(f"[METADATA_UTILS] Erro ao listar tabelas: {e}")
        raise
