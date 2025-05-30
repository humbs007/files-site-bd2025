from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.core.database import get_session
from app.models.table_models import ( # <-- CERTO!
    TableEnelEnergia, TableEnelMeta, TableMeta, TableTelefoniaMeta, TableTelefonia, SearchHistory
)
from app.services.search_service import export_to_csv, export_to_xlsx
from pydantic import BaseModel
from typing import List, Any

router = APIRouter()

# ===========================================
# SCHEMAS DE REQUISIÇÃO
# ===========================================

class FonteSearchRequest(BaseModel):
    table_name: str
    field: str
    operator: str
    term: str

class GeralSearchRequest(BaseModel):
    term: str

# ===========================================
# ROTAS DE SERVIÇO
# ===========================================

@router.get("/tables")
async def list_tables():
    tables = [
        {"label": "Energia - ENEL", "value": "table_enel_energia"},
        {"label": "Meta - ENEL", "value": "table_enel_meta"},
        {"label": "Meta - Endereços", "value": "table_meta"},
        {"label": "Telefonia - Meta", "value": "table_telefonia_meta"},
        {"label": "Telefonia", "value": "table_telefonia"},
    ]
    return tables

@router.get("/tables/{table_name}/fields")
async def list_indexed_fields(table_name: str):
    if table_name == "table_enel_energia":
        fields = ["PN_CPF", "PN_CNPJ", "CC_Conta_Contrato", "INS_Consumo_Estimado", "OL_Bairro_ObjLig", "OL_Regiao"]
    elif table_name == "table_enel_meta":
        fields = ["PN_CPF", "PN_CNPJ"]
    elif table_name == "table_meta":
        fields = ["CPF", "CONSUMO1", "CONSUMO2", "CONSUMO3"]
    elif table_name == "table_telefonia_meta":
        fields = ["cpf_cnpj"]
    elif table_name == "table_telefonia":
        fields = ["cpf_cnpj"]
    else:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")
    return fields

@router.post("/search/fonte")
async def search_by_fonte(request: FonteSearchRequest, db: AsyncSession = Depends(get_session)):
    model = get_model_by_table(request.table_name)
    if model is None:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")

    field_attr = getattr(model, request.field, None)
    if not field_attr:
        raise HTTPException(status_code=404, detail="Campo inválido")

    query = select(model)

    if request.operator == "=":
        query = query.where(field_attr == request.term)
    elif request.operator == ">":
        query = query.where(field_attr > request.term)
    elif request.operator == "<":
        query = query.where(field_attr < request.term)
    elif request.operator == ">=":
        query = query.where(field_attr >= request.term)
    elif request.operator == "<=":
        query = query.where(field_attr <= request.term)
    else:
        raise HTTPException(status_code=400, detail="Operador inválido")

    results = await db.execute(query)
    return results.scalars().all()

@router.post("/search/geral")
async def search_by_geral(request: GeralSearchRequest, db: AsyncSession = Depends(get_session)):
    term = request.term.replace(".", "").replace("-", "").replace("/", "")
    queries = []

    for model, fields in [
        (TableEnelEnergia, ["PN_CPF", "PN_CNPJ"]),
        (TableEnelMeta, ["PN_CPF", "PN_CNPJ"]),
        (TableTelefoniaMeta, ["cpf_cnpj"]),
        (TableTelefonia, ["cpf_cnpj"]),
        (TableMeta, ["CPF"]),
    ]:
        for field in fields:
            field_attr = getattr(model, field, None)
            if field_attr:
                queries.append(select(model).where(field_attr == term))

    results = []
    for q in queries:
        res = await db.execute(q)
        res_list = res.scalars().all()
        if res_list:
            results.append(res_list)

    return results

@router.post("/search/fonte/export/csv")
async def export_search_csv(request: FonteSearchRequest, db: AsyncSession = Depends(get_session)):
    model = get_model_by_table(request.table_name)
    if model is None:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")

    field_attr = getattr(model, request.field, None)
    if not field_attr:
        raise HTTPException(status_code=404, detail="Campo inválido")

    query = select(model)

    if request.operator == "=":
        query = query.where(field_attr == request.term)
    elif request.operator == ">":
        query = query.where(field_attr > request.term)
    elif request.operator == "<":
        query = query.where(field_attr < request.term)
    elif request.operator == ">=":
        query = query.where(field_attr >= request.term)
    elif request.operator == "<=":
        query = query.where(field_attr <= request.term)
    else:
        raise HTTPException(status_code=400, detail="Operador inválido")

    results = await db.execute(query)
    return export_to_csv(results.scalars().all(), filename="buscador_export.csv")

@router.post("/search/fonte/export/xlsx")
async def export_search_xlsx(request: FonteSearchRequest, db: AsyncSession = Depends(get_session)):
    model = get_model_by_table(request.table_name)
    if model is None:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")

    field_attr = getattr(model, request.field, None)
    if not field_attr:
        raise HTTPException(status_code=404, detail="Campo inválido")

    query = select(model)

    if request.operator == "=":
        query = query.where(field_attr == request.term)
    elif request.operator == ">":
        query = query.where(field_attr > request.term)
    elif request.operator == "<":
        query = query.where(field_attr < request.term)
    elif request.operator == ">=":
        query = query.where(field_attr >= request.term)
    elif request.operator == "<=":
        query = query.where(field_attr <= request.term)
    else:
        raise HTTPException(status_code=400, detail="Operador inválido")

    results = await db.execute(query)
    return export_to_xlsx(results.scalars().all(), filename="buscador_export.xlsx")

# ===========================================
# FUNÇÕES AUXILIARES
# ===========================================

def get_model_by_table(table_name: str):
    mapper = {
        "table_enel_energia": TableEnelEnergia,
        "table_enel_meta": TableEnelMeta,
        "table_meta": TableMeta,
        "table_telefonia_meta": TableTelefoniaMeta,
        "table_telefonia": TableTelefonia,
    }
    return mapper.get(table_name)
