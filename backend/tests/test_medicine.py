"""Tests for the Medicine/Treatment Recommendation database and API endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.data.medicine_db import (
    MEDICINE_DB,
    DISEASE_TO_CROPS,
    get_treatment,
    get_all_treatments_for_disease,
    list_diseases_for_crop,
)


# ── Database unit tests ────────────────────────────────────────────────────────

def test_medicine_db_has_all_11_crops():
    expected_crops = {
        "Wheat", "Rice", "Tomato", "Corn", "Potato",
        "Cotton", "Sugarcane", "Soybean", "Mustard", "Groundnut", "Chilli"
    }
    assert set(MEDICINE_DB.keys()) == expected_crops, (
        f"Missing crops: {expected_crops - set(MEDICINE_DB.keys())}"
    )


def test_every_disease_has_three_stages():
    for crop, diseases in MEDICINE_DB.items():
        for disease, stages in diseases.items():
            assert "sowing" in stages, f"[{crop}][{disease}] missing 'sowing'"
            assert "mid_season" in stages, f"[{crop}][{disease}] missing 'mid_season'"
            assert "pre_harvest" in stages, f"[{crop}][{disease}] missing 'pre_harvest'"


def test_every_stage_has_required_fields():
    required = {"chemical", "fungicide", "organic", "dose", "frequency", "notes"}
    for crop, diseases in MEDICINE_DB.items():
        for disease, stages in diseases.items():
            for stage_name, stage_data in stages.items():
                missing = required - set(stage_data.keys())
                assert not missing, (
                    f"[{crop}][{disease}][{stage_name}] missing fields: {missing}"
                )


def test_get_treatment_exact_match():
    t = get_treatment("Wheat", "Yellow Rust", "mid_season")
    assert t is not None
    assert "Propiconazole" in t["chemical"] or "Tebuconazole" in t["chemical"]


def test_get_treatment_case_insensitive():
    t = get_treatment("wheat", "yellow rust", "mid_season")
    assert t is not None


def test_get_treatment_none_for_unknown_crop():
    t = get_treatment("Banana", "Yellow Rust", "mid_season")
    assert t is None


def test_get_treatment_none_for_unknown_disease():
    t = get_treatment("Wheat", "Super Disease XYZ", "sowing")
    assert t is None


def test_get_all_treatments_returns_three_stages():
    all_t = get_all_treatments_for_disease("Rice", "Blast")
    assert all_t is not None
    assert "sowing" in all_t
    assert "mid_season" in all_t
    assert "pre_harvest" in all_t


def test_list_diseases_for_wheat():
    diseases = list_diseases_for_crop("Wheat")
    assert len(diseases) >= 4
    assert "Yellow Rust" in diseases
    assert "Leaf Blight" in diseases


def test_disease_to_crops_lookup():
    crops = DISEASE_TO_CROPS.get("Late Blight", [])
    assert "Tomato" in crops
    assert "Potato" in crops


def test_all_notes_are_nonempty():
    for crop, diseases in MEDICINE_DB.items():
        for disease, stages in diseases.items():
            for stage_name, stage_data in stages.items():
                assert stage_data["notes"].strip(), (
                    f"[{crop}][{disease}][{stage_name}] notes is empty"
                )


# ── API endpoint tests ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_medicine_crops_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/medicine/crops")
    assert r.status_code == 200
    data = r.json()
    assert "crops" in data
    assert "Wheat" in data["crops"]
    assert "Tomato" in data["crops"]
    assert len(data["crops"]) == 11


@pytest.mark.asyncio
async def test_medicine_diseases_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/medicine/diseases?crop=Rice")
    assert r.status_code == 200
    data = r.json()
    assert data["crop"] == "Rice"
    assert "Blast" in data["diseases"]
    assert "Brown Spot" in data["diseases"]


@pytest.mark.asyncio
async def test_medicine_diseases_unknown_crop_returns_404():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/medicine/diseases?crop=Banana")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_medicine_treatment_with_stage():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get(
            "/api/v1/medicine/treatment?crop=Tomato&disease=Late+Blight&stage=mid_season"
        )
    assert r.status_code == 200
    data = r.json()
    assert data["crop"] == "Tomato"
    assert data["disease"] == "Late Blight"
    assert data["stage"] == "mid_season"
    t = data["treatment"]
    assert "chemical" in t
    assert "Metalaxyl" in t["chemical"] or "Dimethomorph" in t["chemical"]


@pytest.mark.asyncio
async def test_medicine_treatment_all_stages():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get(
            "/api/v1/medicine/treatment?crop=Wheat&disease=Yellow+Rust"
        )
    assert r.status_code == 200
    data = r.json()
    assert "all_stages" in data
    assert data["all_stages"]["sowing"] is not None
    assert data["all_stages"]["mid_season"] is not None
    assert data["all_stages"]["pre_harvest"] is not None


@pytest.mark.asyncio
async def test_medicine_treatment_invalid_stage_returns_400():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get(
            "/api/v1/medicine/treatment?crop=Wheat&disease=Yellow+Rust&stage=invalid_stage"
        )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_medicine_treatment_unknown_combination_returns_404():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get(
            "/api/v1/medicine/treatment?crop=Wheat&disease=Unknown+Disease+XYZ"
        )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_medicine_search_by_disease():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/medicine/search?disease=Late+Blight")
    assert r.status_code == 200
    data = r.json()
    assert "Tomato" in data["found_in_crops"]
    assert "Potato" in data["found_in_crops"]
    assert data["total_crops"] >= 2


@pytest.mark.asyncio
async def test_medicine_search_case_insensitive():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/medicine/search?disease=late+blight")
    assert r.status_code == 200
    data = r.json()
    assert data["total_crops"] >= 2


@pytest.mark.asyncio
async def test_medicine_all_crop_disease_combos_return_200():
    """Smoke test: every crop/disease combo must return valid treatment data."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        for crop, diseases in MEDICINE_DB.items():
            for disease in diseases.keys():
                r = await client.get(
                    f"/api/v1/medicine/treatment?crop={crop}&disease={disease}"
                )
                assert r.status_code == 200, (
                    f"Expected 200 for crop={crop}, disease={disease}, got {r.status_code}"
                )
                data = r.json()
                assert data["all_stages"] is not None
