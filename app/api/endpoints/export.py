from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from app.utils.export import generate_export
import io

router = APIRouter()

@router.post("/")  # <-- POST
def export_results(format: str = Body(...), results: dict = Body(...)):
    file_buffer, filename = generate_export(format, results)
    return StreamingResponse(
        file_buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
