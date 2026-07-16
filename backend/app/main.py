from __future__ import annotations

from fastapi import FastAPI

from backend.app.api.routes import router
from backend.app.core.config import load_settings
from backend.app.services.storage import init_db

settings = load_settings()
init_db(settings.data_db_path)

app = FastAPI(title="Aegis Analytics AI")
app.include_router(router)

