import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import alunos, chamadas, auth

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")

app = FastAPI(title="Lista de Chamada — SENAI Limeira")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.exception_handler(Exception)
async def _unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    logging.getLogger(__name__).error("Erro não tratado em %s", request.url, exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor."})


app.include_router(auth.router)
app.include_router(alunos.router)
app.include_router(chamadas.router)
