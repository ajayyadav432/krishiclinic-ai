from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.prediction import Prediction

router = APIRouter()

class OutbreakCluster(BaseModel):
    id: str
    region: str
    district: str
    crop: str
    disease: str
    threat_level: str
    active_cases: int
    trend: str
    radius_km: int
    latitude: float
    longitude: float
    prevention_advisory: str
    last_reported: str

class OutbreakSummaryResponse(BaseModel):
    total_active_clusters: int
    high_risk_alerts: int
    monitored_regions: int
    clusters: List[OutbreakCluster]

class OutbreakAlertSubscription(BaseModel):
    farmer_name: str
    phone_number: str
    district: str
    crops: List[str]
    alert_radius_km: int = 25

class SubscriptionResponse(BaseModel):
    status: str
    message: str
    subscription_id: str

REGIONAL_CLUSTERS = [
    {
        "id": "cluster-jpr-01",
        "region": "Chomu - Amer Belt",
        "district": "Jaipur",
        "crop": "Tomato",
        "disease": "Early Blight",
        "threat_level": "High",
        "active_cases": 24,
        "trend": "Spreading",
        "radius_km": 18,
        "latitude": 27.1726,
        "longitude": 75.7248,
        "prevention_advisory": "High humidity detected. Apply protective copper fungicide spray at 2.5g/L and clear lower leaf debris within 20km perimeter.",
        "last_reported": "10 minutes ago"
    },
    {
        "id": "cluster-kta-02",
        "region": "Hadoti Basin",
        "district": "Kota",
        "crop": "Soybean",
        "disease": "Bacterial Blight",
        "threat_level": "Moderate",
        "active_cases": 15,
        "trend": "Contained",
        "radius_km": 12,
        "latitude": 25.1825,
        "longitude": 75.8391,
        "prevention_advisory": "Avoid overhead irrigation in evening hours. Monitor leaf margins for water-soaked lesions.",
        "last_reported": "35 minutes ago"
    },
    {
        "id": "cluster-alw-03",
        "region": "Tijara Sub-basin",
        "district": "Alwar",
        "crop": "Mustard",
        "disease": "White Rust",
        "threat_level": "Watch",
        "active_cases": 7,
        "trend": "Stable",
        "radius_km": 8,
        "latitude": 27.5530,
        "longitude": 76.6346,
        "prevention_advisory": "Inspect underleaf pustules daily. Ensure adequate field drainage to prevent localized damp spots.",
        "last_reported": "1 hour ago"
    },
    {
        "id": "cluster-skr-04",
        "region": "Danta Ramgarh",
        "district": "Sikar",
        "crop": "Wheat",
        "disease": "Yellow Rust",
        "threat_level": "High",
        "active_cases": 31,
        "trend": "Spreading",
        "radius_km": 25,
        "latitude": 27.6094,
        "longitude": 75.1399,
        "prevention_advisory": "Urgent advisory: Propiconazole 25 EC spray recommended at 1ml/L. Restrict equipment movement across neighboring plots.",
        "last_reported": "15 minutes ago"
    },
    {
        "id": "cluster-bht-05",
        "region": "Bayana Agricultural Zone",
        "district": "Bharatpur",
        "crop": "Potato",
        "disease": "Late Blight",
        "threat_level": "Moderate",
        "active_cases": 12,
        "trend": "Contained",
        "radius_km": 10,
        "latitude": 26.9015,
        "longitude": 77.2917,
        "prevention_advisory": "Mancozeb preventive application recommended for potato fields within 15km perimeter.",
        "last_reported": "2 hours ago"
    }
]

@router.get("/summary", response_model=OutbreakSummaryResponse)
async def get_outbreak_summary(db: AsyncSession = Depends(get_db)):
    high_risk = sum(1 for c in REGIONAL_CLUSTERS if c["threat_level"] == "High")
    unique_districts = len(set(c["district"] for c in REGIONAL_CLUSTERS))
    
    return OutbreakSummaryResponse(
        total_active_clusters=len(REGIONAL_CLUSTERS),
        high_risk_alerts=high_risk,
        monitored_regions=unique_districts,
        clusters=[OutbreakCluster(**c) for c in REGIONAL_CLUSTERS]
    )

@router.post("/subscribe", response_model=SubscriptionResponse)
async def subscribe_outbreak_alerts(payload: OutbreakAlertSubscription):
    sub_id = f"sub-{abs(hash(payload.phone_number + payload.district)) % 1000000}"
    return SubscriptionResponse(
        status="active",
        message=f"Alert subscription configured for {payload.district} radius {payload.alert_radius_km}km",
        subscription_id=sub_id
    )
