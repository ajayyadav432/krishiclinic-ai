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

@pytest.mark.asyncio
async def test_outbreak_summary_reflects_real_predictions():
    import uuid
    from datetime import datetime, timezone
    from app.models.prediction import Prediction
    from app.models.user import User
    from tests.conftest import TestingSessionLocal

    async with TestingSessionLocal() as session:
        user = User(
            id=uuid.uuid4(),
            username="test_farmer_outbreak",
            password_hash="mock_hash",
            role="FARMER"
        )
        session.add(user)
        await session.commit()

        # Insert 3 reviewed predictions for Kota / Bacterial Blight
        for _ in range(3):
            p = Prediction(
                id=uuid.uuid4(),
                crop_type="Soybean",
                image_filename="test_crop.jpg",
                predicted_disease="Bacterial Blight",
                confidence=0.85,
                severity="Medium",
                recommendation="Copper spray 2g/L",
                location="Kota",
                ai_provider="mock",
                status="REVIEWED",
                farmer_id=user.id,
                created_at=datetime.now(timezone.utc),
                reviewed_at=datetime.now(timezone.utc),
            )
            session.add(p)

        # Insert 1 unreviewed (PENDING_REVIEW) prediction (must NOT be counted in active outbreak)
        p_pending = Prediction(
            id=uuid.uuid4(),
            crop_type="Rice",
            image_filename="test_crop.jpg",
            predicted_disease="Blast",
            confidence=0.50,
            severity="Low",
            recommendation="Observe",
            location="Kota",
            ai_provider="mock",
            status="PENDING_REVIEW",
            farmer_id=user.id,
            created_at=datetime.now(timezone.utc),
        )
        session.add(p_pending)

        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/outbreaks/summary")

    assert response.status_code == 200
    data = response.json()
    assert data["total_active_clusters"] >= 1

    # Find the Kota Bacterial Blight cluster
    kota_clusters = [c for c in data["clusters"] if "kota" in c["district"].lower() and "bacterial blight" in c["disease"].lower()]
    assert len(kota_clusters) == 1
    kota_cluster = kota_clusters[0]
    assert kota_cluster["active_cases"] == 3
    assert kota_cluster["threat_level"] in ("Moderate", "High")
    assert kota_cluster["trend"] == "Contained"
    assert "Copper spray" in kota_cluster["prevention_advisory"]

