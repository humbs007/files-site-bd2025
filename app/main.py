from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import metadata, search, export, advanced
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("buscador")

app = FastAPI(
    title="Buscador Multidados V3",
    description="Sistema de busca cruzada entre bases ENEL, META e CREDLINK",
    version="1.0.0"
)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_trace = traceback.format_exc()
    logger.error(f"🔥 ERRO GLOBAL no endpoint {request.url.path}: {str(exc)}")
    logger.debug(f"🧠 STACKTRACE:\n{error_trace}")
    return JSONResponse(
        status_code=500,
        content={"message": "Erro interno no servidor.", "detail": str(exc)}
    )

api_prefix = "/api/v1"
app.include_router(metadata.router, prefix=f"{api_prefix}/tables", tags=["Metadados"])
app.include_router(search.router, prefix=f"{api_prefix}/search", tags=["Busca"])
app.include_router(export.router, prefix=f"{api_prefix}/export", tags=["Exportação"])
app.include_router(advanced.router, prefix=f"{api_prefix}/search", tags=["Busca Avançada"])

@app.get("/")
def root():
    logger.info("🌐 API Online")
    return {"message": "API Online"}