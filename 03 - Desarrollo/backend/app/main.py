from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers import admin, tickets

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    import app.models
    from app.db.base import Base
    from app.db.session import engine

    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Portal de Atención al Cliente API",
    description="Backend del portal empresarial con chatbot IA y reportes mensuales",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets.router)
app.include_router(admin.router)


@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}


_static_dir = Path(settings.static_dir).resolve() if settings.static_dir else None
if _static_dir and _static_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=_static_dir / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def servir_frontend(path: str):
        candidato = (_static_dir / path).resolve()
        if path and candidato.is_file() and candidato.is_relative_to(_static_dir):
            return FileResponse(candidato)
        return FileResponse(_static_dir / "index.html")
