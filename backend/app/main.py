"""FastAPI application entrypoint for Field Shift."""
from __future__ import annotations

import sys
from pathlib import Path

# Add src/ to path so fieldshift package is importable
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.climate import router as climate_router
from .routes.config import router as config_router
from .routes.layers import router as layers_router
from .routes.rotations import router as rotations_router

app = FastAPI(
    title="Field Shift API",
    description="NASA Space Apps Challenge: crop-rotation decision support with NASA climate and satellite data",
    version="1.0.0",
)

# Allow local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local dev & demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router)
app.include_router(climate_router)
app.include_router(rotations_router)
app.include_router(layers_router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Field Shift API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
