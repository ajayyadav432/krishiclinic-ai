import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_translate_offline_fallback():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "text": "Early Blight",
            "target_language": "hi"
        }
        response = await client.post("/api/v1/translate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert len(data["translated_text"]) > 0

@pytest.mark.asyncio
async def test_translate_english_passthrough():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "text": "Powdery Mildew",
            "target_language": "en"
        }
        response = await client.post("/api/v1/translate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["translated_text"] == "Powdery Mildew"
