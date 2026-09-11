import logging
from app.ai.base import AIProvider, PredictionResult

logger = logging.getLogger(__name__)

class FallbackAIProvider(AIProvider):

    def __init__(self, primary: AIProvider, fallback: AIProvider):
        self._primary = primary
        self._fallback = fallback
        self._last_used_provider_name = primary.provider_name

    @property
    def provider_name(self) -> str:
        return self._last_used_provider_name

    async def analyze(
        self,
        image: bytes,
        crop_type: str,
        farmer_notes: str | None = None,
    ) -> PredictionResult:
        try:
            logger.info(f"Attempting crop disease analysis using primary provider: {self._primary.provider_name}")
            result = await self._primary.analyze(image, crop_type, farmer_notes)
            self._last_used_provider_name = self._primary.provider_name
            return result
        except Exception as e:
            logger.warning(
                f"Primary AI provider ({self._primary.provider_name}) failed: {e}. "
                f"Falling back to secondary provider ({self._fallback.provider_name}).",
                exc_info=True
            )
            try:
                result = await self._fallback.analyze(image, crop_type, farmer_notes)
                self._last_used_provider_name = f"{self._primary.provider_name} (fallback to {self._fallback.provider_name})"
                return result
            except Exception as fallback_err:
                logger.error(
                    f"Fallback AI provider ({self._fallback.provider_name}) also failed: {fallback_err}",
                    exc_info=True
                )
                raise fallback_err
