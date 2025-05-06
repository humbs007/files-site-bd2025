# ✅ app/core/metadata_cache.py

from sqlalchemy import inspect
from app.core.database import engine
from app.core.logger import logger
import time

_cache = {}
_cache_ttl = 600  # segundos

def get_cached_tables():
    now = time.time()
    if "tables" in _cache and (now - _cache["timestamp"] < _cache_ttl):
        return _cache["tables"]

    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        _cache["tables"] = tables
        _cache["timestamp"] = now
        logger.info(f"[CACHE] Tabelas atualizadas com sucesso: {len(tables)}")
        return tables
    except Exception as e:
        logger.error(f"[CACHE] Falha ao carregar tabelas: {e}")
        return []
