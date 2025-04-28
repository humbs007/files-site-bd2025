from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.core.database import get_session
from app.models.table_models import (
    TableEnelEnergia, TableEnelMeta, TableMeta, TableTelefoniaMeta, TableTelefonia, SearchHistory
)
from typing import List, Any, Optional
from pydantic import BaseModel
from app.services.search_service import export_to_csv, export_to_xlsx
from app.utils.validators import validate_cpf, validate_cnpj

router = APIRouter()

# ===========================================
# SCHEMAS DE REQUISIÇÃO
# ===========================================

class FonteSearchRequest(BaseModel):
    table_name: str
    field: str
    operator: str
    term: str

class FonteSearchPaginatedRequest(BaseModel):
    table_name: str
    field: str
    operator: str
    term: str
    limit: int = 10
    offset: int = 0

class GeralSearchRequest(BaseModel):
    term: str

# ===========================================
# HELPER PARA MODELOS
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

def standard_response(data: Any = None, message: str = "", status: str = "success"):
    return {"status": status, "message": message, "data": data}

# ===========================================
# ROTAS
# ===========================================

@router.get("/", tags=["Root"])
async def root():
    return standard_response(message="Bem-vindo ao Buscador Multi Dados V2 🚀")

@router.get("/tables", tags=["Tabelas"])
async def list_tables():
    tables = [
        {"label": "Energia - ENEL", "value": "table_enel_energia"},
        {"label": "Meta - ENEL", "value": "table_enel_meta"},
        {"label": "Meta - Endereços", "value": "table_meta"},
        {"label": "Telefonia - Meta", "value": "table_telefonia_meta"},
        {"label": "Telefonia", "value": "table_telefonia"},
    ]
    return standard_response(data=tables)

@router.get("/tables/{table_name}/fields", tags=["Tabelas"])
async def list_indexed_fields(table_name: str):
    fields_mapping = {
        "table_enel_energia": ["PN_CPF", "PN_CNPJ", "CC_Conta_Contrato", "INS_Consumo_Estimado", "OL_Bairro_ObjLig", "OL_Regiao"],
        "table_enel_meta": ["PN_CPF", "PN_CNPJ"],
        "table_meta": ["CPF", "CONSUMO1", "CONSUMO2", "CONSUMO3"],
        "table_telefonia_meta": ["cpf_cnpj"],
        "table_telefonia": ["cpf_cnpj"],
    }
    fields = fields_mapping.get(table_name)
    if not fields:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")
    return standard_response(data=fields)

@router.post("/search/fonte", tags=["Busca Fonte"])
async def search_by_fonte(
    request: FonteSearchPaginatedRequest,
    db: AsyncSession = Depends(get_session)
):
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

    query = query.offset(request.offset).limit(request.limit)

    results = await db.execute(query)
    rows = results.scalars().all()

    return standard_response(data=[r.__dict__ for r in rows])

@router.post("/search/geral", tags=["Busca Geral"])
async def search_by_geral(
    request: GeralSearchRequest,
    db: AsyncSession = Depends(get_session)
):
    term = request.term.replace(".", "").replace("-", "").replace("/", "").strip()

    if len(term) == 11:
        validate_cpf(term)
    elif len(term) == 14:
        validate_cnpj(term)
    else:
        raise HTTPException(status_code=400, detail="CPF ou CNPJ inválido")

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
            results.append([r.__dict__ for r in res_list])

    return standard_response(data=results)

@router.post("/search/fonte/export/csv", tags=["Exportação"])
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

@router.post("/search/fonte/export/xlsx", tags=["Exportação"])
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
