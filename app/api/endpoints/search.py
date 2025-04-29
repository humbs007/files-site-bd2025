from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.connection import get_connection
from app.utils.validators import get_indexed_fields, validate_operator

router = APIRouter()

class SearchOption1Request(BaseModel):
    tables: list[str]
    field: str
    operator: str
    term: str

class SearchOption2Request(BaseModel):
    number: str

@router.post("/option1")
def search_option1(data: SearchOption1Request):
    if not validate_operator(data.operator):
        raise HTTPException(status_code=400, detail="Operador inválido")

    results = []

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    for table in data.tables:
        indexed_fields = get_indexed_fields(table)
        if data.field not in indexed_fields:
            continue

        query = f"SELECT * FROM {table} WHERE {data.field} {data.operator} %s"
        cursor.execute(query, (data.term,))
        rows = cursor.fetchall()
        if rows:
            results.append({"table": table, "data": rows})

    cursor.close()
    conn.close()
    return {"results": results}

@router.post("/option2")
def search_option2(data: SearchOption2Request):
    number = data.number
    results = {}

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SHOW TABLES")
    tables = [row[f'Tables_in_{conn.database}'] for row in cursor.fetchall()]

    for table in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = [col["Field"] for col in cursor.fetchall()]
        cpf_cnpj_fields = [c for c in columns if "cpf" in c.lower() or "cnpj" in c.lower()]
        for field in cpf_cnpj_fields:
            query = f"SELECT * FROM {table} WHERE {field} = %s"
            cursor.execute(query, (number,))
            rows = cursor.fetchall()
            if rows:
                results.setdefault(table, []).extend(rows)

    cursor.close()
    conn.close()
    return {"results": results}
