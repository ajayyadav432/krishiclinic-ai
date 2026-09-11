import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_outbreak_summary():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/outbreaks/summary")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_active_clusters" in data
    assert "high_risk_alerts" in data
    assert "monitored_regions" in data
    assert "clusters" in data
    assert len(data["clusters"]) > 0
    
    first = data["clusters"][0]
    assert "id" in first
    assert "region" in first
    assert "district" in first
    assert "crop" in first
    assert "disease" in first
    assert "threat_level" in first
    assert "radius_km" in first
    assert "prevention_advisory" in first

@pytest.mark.asyncio
async def test_outbreak_subscription():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "farmer_name": "Ramesh Kumar",
            "phone_number": "9876543210",
            "district": "Jaipur",
            "crops": ["Tomato", "Wheat"],
            "alert_radius_km": 20
        }
        response = await client.post("/api/v1/outbreaks/subscribe", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert "subscription_id" in data
    assert "Jaipur" in data["message"]
