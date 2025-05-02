from fastapi import APIRouter
from sqlalchemy import inspect
from app.core.config import engine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

LABEL_MAP = {
    "CPF": "CPF",
    "PN_CPF": "CPF",
    "PN_CNPJ": "CNPJ",
    "NOME": "Nome Completo",
    "DT_NASCIMENTO": "Data de Nascimento",
    "RENDA_PRESUMIDA": "Renda Presumida",
    "FAIXA_RENDA": "Faixa de Renda",
    "PN_Nome": "Nome",
    "INS_Consumo_Estimado": "Consumo Estimado",
    "PN_RG": "RG",
    "EMAIL": "E-mail",
    "PN_Email": "E-mail",
    "CIDADE": "Cidade",
    "UF": "UF",
    "STATUS_RECEITA_FEDERAL": "Situação Receita Federal",
    "FLAG_OBITO": "Óbito",
    # adicione mais campos conforme necessário...
}

@router.get("/metadata", tags=["Metadados"])
def get_metadata():
    try:
        inspector = inspect(engine)
        result = {}

        for table_name in inspector.get_table_names():
            indexed_fields = []

            for index in inspector.get_indexes(table_name):
                for col in index.get("column_names", []):
                    indexed_fields.append(col)

            # remove duplicatas e adiciona label amigável
            clean_fields = list(set(indexed_fields))
            formatted = [
                {"name": field, "label": LABEL_MAP.get(field, field.replace("_", " ").title())}
                for field in clean_fields
            ]
            result[table_name] = sorted(formatted, key=lambda x: x["label"])

        return {"tables": result}
    except Exception as e:
        logger.error(f"[METADATA] Erro ao buscar metadados: {e}")
        return {"tables": {}}
