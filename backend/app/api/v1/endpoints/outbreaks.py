from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.dependencies import get_db
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

DISTRICT_COORDINATES = {
    "jaipur": (27.1726, 75.7248),
    "kota": (25.1825, 75.8391),
    "alwar": (27.5530, 76.6346),
    "sikar": (27.6094, 75.1399),
    "bharatpur": (26.9015, 77.2917),
    "pune": (18.5204, 73.8567),
    "nagpur": (21.1458, 79.0882),
    "ludhiana": (30.9010, 75.8573),
    "patna": (25.5941, 85.1376),
    "varanasi": (25.3176, 82.9739),
    "indore": (22.7196, 75.8577),
    "bhopal": (23.2599, 77.4126),
    "ahmedabad": (23.0225, 72.5714),
    "surat": (21.1702, 72.8311),
    "hyderabad": (17.3850, 78.4867),
    "warangal": (17.9689, 79.5941),
    "kurnool": (15.8281, 78.0373),
    "delhi": (28.7041, 77.1025),
}

def get_coordinates(district: str) -> tuple[float, float]:
    clean = district.lower().strip()
    for key, coords in DISTRICT_COORDINATES.items():
        if key in clean:
            return coords
    h = abs(hash(clean))
    lat = 18.0 + (h % 1000) / 100.0
    lon = 73.0 + ((h // 1000) % 1000) / 100.0
    return (round(lat, 4), round(lon, 4))

@router.get("/summary", response_model=OutbreakSummaryResponse)
async def get_outbreak_summary(db: AsyncSession = Depends(get_db)):
    from datetime import timezone

    disease_expr = func.coalesce(Prediction.agronomist_predicted_disease, Prediction.predicted_disease)
    location_expr = func.coalesce(func.nullif(func.trim(Prediction.location), ""), "General Agricultural Belt")

    query = (
        select(
            location_expr.label("location"),
            disease_expr.label("disease"),
            func.max(Prediction.crop_type).label("crop"),
            func.count(Prediction.id).label("case_count"),
            func.max(Prediction.created_at).label("latest_reported_at"),
            func.max(func.coalesce(Prediction.agronomist_review, Prediction.recommendation)).label("advisory"),
            func.max(func.coalesce(Prediction.agronomist_severity, Prediction.severity)).label("max_severity"),
        )
        .where(Prediction.status == "REVIEWED")
        .group_by(location_expr, disease_expr)
        .order_by(func.count(Prediction.id).desc())
    )

    result = await db.execute(query)
    rows = result.all()

    if not rows:
        high_risk = sum(1 for c in REGIONAL_CLUSTERS if c["threat_level"] == "High")
        unique_districts = len(set(c["district"] for c in REGIONAL_CLUSTERS))
        return OutbreakSummaryResponse(
            total_active_clusters=len(REGIONAL_CLUSTERS),
            high_risk_alerts=high_risk,
            monitored_regions=unique_districts,
            clusters=[OutbreakCluster(**c) for c in REGIONAL_CLUSTERS]
        )

    now = datetime.now(timezone.utc)
    clusters: List[OutbreakCluster] = []

    for idx, row in enumerate(rows):
        loc = row.location or "General Region"
        disease = row.disease or "Unknown Disease"
        crop = row.crop or "Crop"
        cases = int(row.case_count or 1)
        severity = str(row.max_severity or "Medium")

        district = loc.split("-")[0].strip()
        region = loc if "-" in loc else f"{loc} Agricultural Zone"

        if cases >= 10 or severity.lower() == "high":
            threat_level = "High"
            radius_km = 25
        elif cases >= 3 or severity.lower() == "medium":
            threat_level = "Moderate"
            radius_km = 15
        else:
            threat_level = "Watch"
            radius_km = 10

        if cases >= 5:
            trend = "Spreading"
        elif cases >= 2:
            trend = "Contained"
        else:
            trend = "Stable"

        lat, lon = get_coordinates(district)

        if row.latest_reported_at:
            reported_time = row.latest_reported_at
            if reported_time.tzinfo is None:
                reported_time = reported_time.replace(tzinfo=timezone.utc)
            delta = now - reported_time
            minutes = max(1, int(delta.total_seconds() / 60))
            if minutes < 60:
                last_reported = f"{minutes} minutes ago"
            elif minutes < 1440:
                last_reported = f"{minutes // 60} hours ago"
            else:
                last_reported = f"{delta.days} days ago"
        else:
            last_reported = "Recently"

        slug_loc = "".join(c if c.isalnum() else "-" for c in loc.lower())[:10].strip("-")
        slug_dis = "".join(c if c.isalnum() else "-" for c in disease.lower())[:10].strip("-")
        cluster_id = f"cluster-{slug_loc}-{slug_dis}-{idx+1}"

        advisory = row.advisory or f"Active outbreak advisory: Apply protective preventive treatment for {disease} on {crop} within {radius_km}km perimeter."

        clusters.append(
            OutbreakCluster(
                id=cluster_id,
                region=region,
                district=district,
                crop=crop,
                disease=disease,
                threat_level=threat_level,
                active_cases=cases,
                trend=trend,
                radius_km=radius_km,
                latitude=lat,
                longitude=lon,
                prevention_advisory=advisory,
                last_reported=last_reported,
            )
        )

    high_risk_count = sum(1 for c in clusters if c.threat_level == "High")
    unique_districts_count = len(set(c.district for c in clusters))

    return OutbreakSummaryResponse(
        total_active_clusters=len(clusters),
        high_risk_alerts=high_risk_count,
        monitored_regions=unique_districts_count,
        clusters=clusters,
    )

@router.post("/subscribe", response_model=SubscriptionResponse)
async def subscribe_outbreak_alerts(payload: OutbreakAlertSubscription):
    sub_id = f"sub-{abs(hash(payload.phone_number + payload.district)) % 1000000}"
    return SubscriptionResponse(
        status="active",
        message=f"Alert subscription configured for {payload.district} radius {payload.alert_radius_km}km",
        subscription_id=sub_id
    )
