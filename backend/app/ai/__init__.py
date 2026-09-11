from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

class PredictionResult(BaseModel):

    predicted_disease: str = Field(description="Name of the identified disease")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0"
    )
    severity: str = Field(description="Severity level: Low, Medium, or High")
    recommendation: str = Field(description="Actionable treatment recommendation")

class AIProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...

    @abstractmethod
    async def analyze(
        self,
        image: bytes,
        crop_type: str,
        farmer_notes: str | None = None,
    ) -> PredictionResult:
        ...
