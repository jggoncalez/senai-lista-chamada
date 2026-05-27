import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import turmas, alunos, chamadas, usuarios, cursos, turma_disciplinas, sessoes, auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Backend SENAI iniciado — conectado ao Azure SQL Database")
    yield
    logger.info("Backend SENAI encerrado")


app = FastAPI(
    title="Lista de Chamada — SENAI",
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cursos.router)
app.include_router(turmas.router)
app.include_router(alunos.router)
app.include_router(usuarios.router)
app.include_router(turma_disciplinas.router)
app.include_router(sessoes.router)
app.include_router(chamadas.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
