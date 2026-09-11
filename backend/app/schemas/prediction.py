from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

class PredictionResponse(BaseModel):

    id: UUID
    crop_type: str
    image_filename: str | None = None
    farmer_notes: str | None = None
    predicted_disease: str
    confidence: float = Field(ge=0.0, le=1.0)
    severity: str | None = None
    recommendation: str | None = None
    ai_provider: str
    created_at: datetime
    
    farmer_id: UUID | None = None
    agronomist_id: UUID | None = None
    status: str
    agronomist_review: str | None = None
    agronomist_predicted_disease: str | None = None
    agronomist_severity: str | None = None
    reviewed_at: datetime | None = None

    possible_reasons: str | None = None
    location: str | None = None
    language: str | None = None

    after_image_filename: str | None = None
    after_notes: str | None = None
    after_uploaded_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class PredictionListItem(BaseModel):

    id: UUID
    crop_type: str
    image_filename: str | None = None
    predicted_disease: str
    confidence: float = Field(ge=0.0, le=1.0)
    severity: str | None = None
    ai_provider: str
    created_at: datetime
    status: str
    farmer_id: UUID | None = None
    agronomist_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)

class AgronomistReviewRequest(BaseModel):

    predicted_disease: str = Field(..., min_length=1, max_length=150, description="Verified disease name")
    severity: str = Field(..., description="Verified severity level (Low, Medium, High)")
    review: str = Field(..., min_length=1, description="Treatment recommendation or advisory comments")

class PredictionListResponse(BaseModel):

    items: list[PredictionListItem]
    total: int
    page: int
    limit: int

class DiseaseCount(BaseModel):

    disease: str
    count: int

class DailyCount(BaseModel):

    date: str
    count: int

class AnalyticsSummaryResponse(BaseModel):

    total_predictions: int
    average_confidence: float
    disease_distribution: list[DiseaseCount]
    daily_volume: list[DailyCount]
    severity_distribution: dict[str, int]
    top_crop: str | None = None

class HealthResponse(BaseModel):

    status: str
    version: str
    database: str
