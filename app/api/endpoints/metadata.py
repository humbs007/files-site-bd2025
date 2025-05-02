from fastapi import APIRouter
from app.core.config import engine
from sqlalchemy import inspect
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

FIELD_LABELS = {
    "PN_CPF": "CPF (ENEL)",
    "PN_CNPJ": "CNPJ (ENEL)",
    "CPF": "CPF",
    "CONSUMO": "Consumo (META)",
    "CELULAR1": "Celular 1",
    "TEL_FIXO1": "Telefone Fixo 1",
    "NOME": "Nome Completo",
    "NOME_MAE": "Nome da Mãe",
    "DT_NASCIMENTO": "Data de Nascimento",
    "RENDA_PRESUMIDA": "Renda Presumida"
}

def map_label(field):
    return FIELD_LABELS.get(field, field.replace("_", " ").capitalize())

@router.get("/")
def get_metadata():
    try:
        metadata = {}
        inspector = inspect(engine)
        valid_tables = ["table_enel", "table_meta", "table_credlink"]
        all_fields_set = set()

        for table in valid_tables:
            indexes = [i['column_names'][0] for i in inspector.get_indexes(table) if 'column_names' in i]

            if table == "table_meta":
                indexes = ['CONSUMO' if f.startswith("CONSUMO") else f for f in indexes]

            metadata[table] = indexes
            all_fields_set.update(indexes)

        metadata["TODAS"] = sorted(list(all_fields_set))
        return {"tables": metadata}

    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar metadados: {e}")
        return {"tables": {}}
