# ✅ backend/app/api/endpoints/metadata.py

from fastapi import APIRouter
from sqlalchemy import inspect
from app.core.logger import logger
from app.core.config import engine
from app.core.db_schema_config import DB_SCHEMA, UNIFIED_KEYS  # 👈 NOVO

router = APIRouter()


@router.get("", tags=["Metadados"])
def list_tables():
    """🔍 Retorna todas as tabelas reais do banco de dados."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"[METADATA] {len(tables)} tabelas carregadas com sucesso.")
        return {"tables": tables}
    except Exception as e:
        logger.error(f"[METADATA] Erro ao listar tabelas: {e}")
        return {"tables": []}


@router.get("/{table_name}/fields", tags=["Metadados"])
def list_table_fields(table_name: str):
    """📦 Retorna os campos indexados da tabela especificada (PK + índices)."""
    try:
        inspector = inspect(engine)

        pk_columns = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
        indexes = inspector.get_indexes(table_name)

        indexed_columns = set(pk_columns)
        for index in indexes:
            indexed_columns.update(index.get("column_names", []))

        indexed_list = sorted(indexed_columns)
        logger.info(f"[METADATA] {len(indexed_list)} campos indexados encontrados para {table_name}.")
        return {"fields": indexed_list}

    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar campos indexados de '{table_name}': {e}")
        return {"fields": []}


@router.get("/fields/comuns", tags=["Metadados"])
def get_common_fields():
    """🔁 Retorna os campos unificados usados em buscas cruzadas."""
    try:
        if not UNIFIED_KEYS:
            logger.warning("[METADATA] Nenhum campo unificado encontrado em UNIFIED_FIELDS.")
            return {"fields": []}

        logger.info(f"[METADATA] Campos comuns disponíveis via unificados: {UNIFIED_KEYS}")
        return {"fields": sorted(UNIFIED_KEYS)}
    except Exception as e:
        logger.error(f"[METADATA] Erro ao obter campos comuns: {e}")
        return {"fields": []}


@router.get("/labels/{table}/{field}", tags=["Metadados"])
def get_friendly_label(table: str, field: str):
    """🎯 Retorna nome amigável do campo com fallback para o nome real."""
    try:
        label = DB_SCHEMA.get("tabelas", {}).get(table, {}).get("campos", {}).get(field, field)
        return {"label": label}
    except Exception as e:
        logger.warning(f"[METADATA] Erro ao buscar label para {table}.{field}: {e}")
        return {"label": field}


@router.get("/full", tags=["Metadados"])
def get_full_schema():
    """🧠 Retorna schema estático para debug/dev."""
    return DB_SCHEMA
