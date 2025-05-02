from fastapi import APIRouter
from sqlalchemy import inspect
from app.core.config import engine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/tables", tags=["Metadados"])
def list_tables():
    """Retorna lista de tabelas disponíveis no banco."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return {"tables": tables}
    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar tabelas: {e}")
        return {"tables": []}


@router.get("/tables/{table_name}/fields", tags=["Metadados"])
def list_table_fields(table_name: str):
    """Retorna os campos indexados de uma tabela específica."""
    try:
        inspector = inspect(engine)
        indexes = inspector.get_indexes(table_name)
        indexed_fields = []

        for index in indexes:
            for col in index.get("column_names", []):
                if col not in indexed_fields:
                    indexed_fields.append(col)

        return {"fields": sorted(indexed_fields)}
    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar campos da tabela {table_name}: {e}")
        return {"fields": []}


@router.get("/tables/fields/comuns", tags=["Metadados"])
def get_common_fields():
    """
    Retorna campos comuns a todas as tabelas, exemplo: CPF, PN_CPF, CNPJ etc.
    Esses são usados quando 'TODAS' as tabelas são selecionadas.
    """
    try:
        # Campos indexados usados em todas as tabelas
        fields = ['CPF', 'PN_CPF', 'CNPJ', 'PN_CNPJ']
        return {"fields": sorted(list(set(fields)))}
    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar campos comuns: {e}")
        return {"fields": []}
