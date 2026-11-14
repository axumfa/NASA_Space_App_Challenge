"""Integration tests for FastAPI endpoints."""
from __future__ import annotations

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_config():
    resp = client.get("/api/config")
    assert resp.status_code == 200
    data = resp.json()
    assert "demo_fields" in data
    assert "fergana" in data["demo_fields"]
    assert "crops" in data
    assert "winter_wheat" in data["crops"]
    assert "cotton" in data["crops"]
    assert "translations" in data
    assert "glossary" in data


def test_presets():
    resp = client.get("/api/presets")
    assert resp.status_code == 200
    presets = resp.json()
    assert len(presets) >= 2
    keys = [p["key"] for p in presets]
    assert "fergana" in keys
    assert "kansas" in keys


def test_layers_gibs():
    resp = client.get("/api/layers/gibs")
    assert resp.status_code == 200
    layers = resp.json()
    assert len(layers) >= 4
    keys = [l["key"] for l in layers]
    assert "ndvi" in keys
    assert "precip" in keys
    assert "temp" in keys
    assert "soil" in keys


def test_context_fergana():
    # Fergana coordinates from committed demo cache
    resp = client.post(
        "/api/context",
        json={"lat": 40.4229, "lon": 71.7576, "rain_pct": 0, "temp_c": 0.0},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["field_key"] == "fergana"
    assert data["kpis"]["rain_median"] > 0
    assert len(data["monthly_climatology"]) == 12
    assert len(data["sources"]) == 4


def test_rotations_evaluate_fergana():
    resp = client.post(
        "/api/rotations/evaluate",
        json={
            "lat": 40.4229,
            "lon": 71.7576,
            "rain_pct": 0,
            "temp_c": 0.0,
            "current_crops": ["winter_wheat", "cotton"],
            "irrigation_supply": 1.0,
            "weights": {
                "water_saving": 5,
                "soil_om": 5,
                "nitrogen": 5,
                "erosion": 5,
                "forage": 5,
                "income": 5,
            },
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "options" in data
    assert len(data["options"]) >= 2
    cur = data["options"][0]
    assert cur["is_current"] is True
    assert cur["crops"] == ["winter_wheat", "cotton"]
    assert "radar_scores" in cur
    assert "summary_box" in data
