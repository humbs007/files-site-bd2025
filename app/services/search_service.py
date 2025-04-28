import pandas as pd
from fastapi.responses import StreamingResponse
import io
from typing import List, Any

# Função para exportar para CSV
def export_to_csv(results: List[Any], filename: str = "export.csv"):
    df = pd.DataFrame([r.__dict__ for r in results])
    df.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")
    stream = io.StringIO()
    df.to_csv(stream, index=False, encoding="utf-8-sig")
    response = StreamingResponse(iter([stream.getvalue()]),
                                  media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

# Função para exportar para XLSX
def export_to_xlsx(results: List[Any], filename: str = "export.xlsx"):
    df = pd.DataFrame([r.__dict__ for r in results])
    df.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Resultados")
    output.seek(0)
    response = StreamingResponse(iter([output.read()]),
                                  media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response
