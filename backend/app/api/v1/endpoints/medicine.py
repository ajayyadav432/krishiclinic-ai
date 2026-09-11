"""Medicine / Treatment Recommendation API endpoint.

Provides stage-wise fungicide and treatment lookup for crop diseases.
Used by the Agronomist Portal to quickly fill in treatment advisories.
"""

import logging
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.data.medicine_db import (
    MEDICINE_DB,
    DISEASE_TO_CROPS,
    get_treatment,
    get_all_treatments_for_disease,
    list_diseases_for_crop,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class TreatmentDetail(BaseModel):
    chemical: str
    fungicide: str
    organic: str
    dose: str
    frequency: str
    notes: str


class AllStagesTreatment(BaseModel):
    sowing: Optional[TreatmentDetail] = None
    mid_season: Optional[TreatmentDetail] = None
    pre_harvest: Optional[TreatmentDetail] = None


class MedicineResponse(BaseModel):
    crop: str
    disease: str
    stage: Optional[str] = None
    treatment: Optional[TreatmentDetail] = None
    all_stages: Optional[AllStagesTreatment] = None


class CropListResponse(BaseModel):
    crops: list[str]


class DiseaseListResponse(BaseModel):
    crop: str
    diseases: list[str]


@router.get(
    "/medicine/crops",
    response_model=CropListResponse,
    summary="List supported crops",
    description="Returns list of all crops with treatment data in the medicine database.",
    tags=["Medicine"],
)
async def list_crops():
    return CropListResponse(crops=sorted(MEDICINE_DB.keys()))


@router.get(
    "/medicine/diseases",
    response_model=DiseaseListResponse,
    summary="List diseases for a crop",
    description="Returns list of diseases with treatment data for a given crop.",
    tags=["Medicine"],
)
async def list_diseases(
    crop: str = Query(..., description="Crop name (e.g., Wheat, Rice, Tomato)")
):
    diseases = list_diseases_for_crop(crop)
    if not diseases:
        raise HTTPException(
            status_code=404,
            detail=f"No treatment data found for crop '{crop}'. "
                   f"Available crops: {', '.join(sorted(MEDICINE_DB.keys()))}",
        )
    return DiseaseListResponse(crop=crop.title(), diseases=diseases)


@router.get(
    "/medicine/treatment",
    response_model=MedicineResponse,
    summary="Get treatment recommendation",
    description=(
        "Returns stage-wise treatment (chemical, fungicide, organic, dose, frequency, notes) "
        "for a crop-disease pair. "
        "Stage options: 'sowing', 'mid_season', 'pre_harvest'. "
        "If stage is omitted, returns all stages."
    ),
    tags=["Medicine"],
)
async def get_medicine(
    crop: str = Query(..., description="Crop name (e.g., Wheat, Tomato, Rice)"),
    disease: str = Query(..., description="Disease name (e.g., Yellow Rust, Late Blight)"),
    stage: Optional[str] = Query(
        None,
        description="Growth stage: 'sowing', 'mid_season', 'pre_harvest'. "
                    "Omit to get all stages.",
    ),
):
    valid_stages = {"sowing", "mid_season", "pre_harvest"}

    if stage and stage not in valid_stages:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid stage '{stage}'. Valid stages: {', '.join(valid_stages)}",
        )

    if stage:
        treatment = get_treatment(crop, disease, stage)
        if treatment is None:
            raise HTTPException(
                status_code=404,
                detail=f"No treatment data found for crop='{crop}', disease='{disease}', stage='{stage}'.",
            )
        return MedicineResponse(
            crop=crop.title(),
            disease=disease.title(),
            stage=stage,
            treatment=TreatmentDetail(**treatment),
        )
    else:
        all_data = get_all_treatments_for_disease(crop, disease)
        if all_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"No treatment data found for crop='{crop}', disease='{disease}'. "
                       f"Use /api/v1/medicine/diseases?crop={crop} to see available diseases.",
            )
        all_stages = AllStagesTreatment(
            sowing=TreatmentDetail(**all_data["sowing"]) if "sowing" in all_data else None,
            mid_season=TreatmentDetail(**all_data["mid_season"]) if "mid_season" in all_data else None,
            pre_harvest=TreatmentDetail(**all_data["pre_harvest"]) if "pre_harvest" in all_data else None,
        )
        return MedicineResponse(
            crop=crop.title(),
            disease=disease.title(),
            all_stages=all_stages,
        )


@router.get(
    "/medicine/search",
    summary="Search treatment by disease name",
    description="Find which crops have treatment data for a given disease.",
    tags=["Medicine"],
)
async def search_by_disease(
    disease: str = Query(..., description="Disease name to search for"),
):
    disease_key = disease.strip().title()
    # Try exact match first
    crops = DISEASE_TO_CROPS.get(disease_key, [])
    if not crops:
        # Try case-insensitive
        for k, v in DISEASE_TO_CROPS.items():
            if k.lower() == disease.strip().lower():
                crops = v
                disease_key = k
                break
    return {
        "disease": disease_key or disease,
        "found_in_crops": crops,
        "total_crops": len(crops),
    }
