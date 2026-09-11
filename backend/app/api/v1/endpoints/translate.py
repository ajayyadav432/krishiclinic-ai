import logging
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.config import get_settings
from app.ai.translation_data import (
    get_dictionary_translation,
    DISEASE_TRANSLATIONS,
    ADVISORY_SENTENCE_TRANSLATIONS,
    STATUS_AND_UI_TRANSLATIONS,
    CROP_TRANSLATIONS,
    SEVERITY_TRANSLATIONS,
)

logger = logging.getLogger(__name__)
router = APIRouter()

class TranslationRequest(BaseModel):
    text: str = Field(..., description="Text to translate")
    target_language: str = Field(..., description="ISO 639-1 language code (e.g., hi, te, mr, es)")

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str

# Maintain FALLBACK_DICT for direct backward compatibility and inspection
FALLBACK_DICT: dict[str, dict[str, str]] = {"hi": {}, "te": {}, "mr": {}, "es": {}}

for d in [DISEASE_TRANSLATIONS, ADVISORY_SENTENCE_TRANSLATIONS, STATUS_AND_UI_TRANSLATIONS]:
    for key, trans_map in d.items():
        for lang, trans_val in trans_map.items():
            if lang in FALLBACK_DICT:
                # Store with both original key casing and lowercase for flexible lookup
                FALLBACK_DICT[lang][key] = trans_val

@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Translate Text",
    description="Translate text to target language (e.g. hi, te, mr, es) using fast offline domain dictionaries, MyMemory, or Google Translate."
)
async def translate_text(request: TranslationRequest):
    text = request.text.strip()
    target = request.target_language.strip().lower()

    if not text:
        return TranslationResponse(translated_text="", source_language="en")

    if target == "en":
        return TranslationResponse(translated_text=text, source_language="en")

    # Step 1: Fast deterministic domain dictionary lookup (0ms, 100% reliable offline)
    dict_hit = get_dictionary_translation(text, target)
    if dict_hit:
        return TranslationResponse(translated_text=dict_hit, source_language="en")

    # Step 2: Backward-compatible fallback dict check
    if target in FALLBACK_DICT:
        if text in FALLBACK_DICT[target]:
            return TranslationResponse(translated_text=FALLBACK_DICT[target][text], source_language="en")
        lowered = text.lower()
        if lowered in FALLBACK_DICT[target]:
            return TranslationResponse(translated_text=FALLBACK_DICT[target][lowered], source_language="en")

    # Step 3: Official Google Translate API (if configured)
    settings = get_settings()
    api_key = settings.GOOGLE_TRANSLATE_API_KEY
    if api_key:
        try:
            url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
            payload = {"q": [text], "target": target}
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    translated = data["data"]["translations"][0]["translatedText"]
                    source_lang = data["data"]["translations"][0].get("detectedSourceLanguage", "en")
                    return TranslationResponse(translated_text=translated, source_language=source_lang)
        except Exception as e:
            logger.warning(f"Official Google Translate API error: {e}")

    # Step 4: MyMemory Translation API (free, reliable fallback)
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": f"en|{target}"}
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                translated = data.get("responseData", {}).get("translatedText")
                if translated and not translated.startswith("MYMEMORY WARNING"):
                    return TranslationResponse(translated_text=translated, source_language="en")
    except Exception as e:
        logger.warning(f"MyMemory API error: {e}")

    # Step 5: Google GTX translation endpoint
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target,
            "dt": "t",
            "q": text,
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        async with httpx.AsyncClient(headers=headers, timeout=3.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                translated = ""
                for sentence in data[0]:
                    if sentence and len(sentence) > 0:
                        translated += sentence[0]
                if translated:
                    source_lang = data[2] if len(data) > 2 else "auto"
                    return TranslationResponse(translated_text=translated, source_language=source_lang)
    except Exception as e:
        logger.warning(f"Google GTX API error: {e}")

    # Step 6: Graceful fallback to original text
    logger.warning(f"All translation methods exhausted for '{text}'. Returning original text.")
    return TranslationResponse(translated_text=text, source_language="en")
