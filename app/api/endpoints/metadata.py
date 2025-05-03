from fastapi import APIRouter
from sqlalchemy import inspect
from app.core.config import engine
from app.core.logger import logger

router = APIRouter()


@router.get("", tags=["Metadados"])  # 🔧 Corrigido para raiz do endpoint
def list_tables():
    """🔍 Retorna todas as tabelas do banco."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"[METADATA] {len(tables)} tabelas carregadas com sucesso.")
        return {"tables": tables}
    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar tabelas: {e}")
        return {"tables": []}


@router.get("/{table_name}/fields", tags=["Metadados"])
def list_table_fields(table_name: str):
    """📦 Retorna os campos indexados de uma tabela específica."""
    try:
        inspector = inspect(engine)
        indexes = inspector.get_indexes(table_name)
        indexed_fields = []

        for index in indexes:
            for col in index.get("column_names", []):
                if col not in indexed_fields:
                    indexed_fields.append(col)

        logger.info(f"[METADATA] Tabela '{table_name}': {len(indexed_fields)} campos indexados encontrados.")
        return {"fields": sorted(indexed_fields)}

    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar campos da tabela '{table_name}': {e}")
        return {"fields": []}


@router.get("/fields/comuns", tags=["Metadados"])
def get_common_fields():
    """
    🔁 Retorna todos os campos indexados de todas as tabelas — busca geral (TODAS).
    """
    try:
        inspector = inspect(engine)
        all_tables = inspector.get_table_names()
        field_set = set()

        for table in all_tables:
            try:
                indexes = inspector.get_indexes(table)
                for index in indexes:
                    for col in index.get("column_names", []):
                        field_set.add(col)
            except Exception as table_error:
                logger.warning(f"[METADATA] Falha ao processar índices da tabela '{table}': {table_error}")

        sorted_fields = sorted(field_set)
        logger.info(f"[METADATA] {len(sorted_fields)} campos comuns agregados a partir de {len(all_tables)} tabelas.")
        return {"fields": sorted_fields}

    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar campos comuns: {e}")
        return {"fields": []}
