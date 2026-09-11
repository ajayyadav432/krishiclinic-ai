from fastapi import APIRouter
from app.api.v1.endpoints import health, predictions, analytics, export, auth, translate, comments, outbreaks

router = APIRouter()

router.include_router(health.router, tags=["Health"])
router.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
router.include_router(translate.router, prefix="/api/v1", tags=["Translation"])
router.include_router(export.router, prefix="/api/v1", tags=["Export"])
router.include_router(predictions.router, prefix="/api/v1", tags=["Predictions"])
router.include_router(comments.router, prefix="/api/v1", tags=["Comments"])
router.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
router.include_router(outbreaks.router, prefix="/api/v1/outbreaks", tags=["Outbreaks"])
