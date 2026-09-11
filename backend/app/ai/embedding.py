import os
import hmac
import hashlib
import logging
import asyncio
from google import genai

from app.core.config import get_settings

import re
import math

logger = logging.getLogger(__name__)

def get_mock_embedding(text: str) -> list[float]:
    """
    Generate a 768-dimensional normalized feature-hashed embedding (Bag-of-Words + Subword n-grams).
    Provides meaningful cosine similarity for shared agronomic terms, crops, and symptoms in mock mode.
    """
    vector = [0.0] * 768
    if not text:
        return vector

    tokens = re.findall(r"\w+", text.lower().strip())
    if not tokens:
        return vector

    features = list(tokens)
    for token in tokens:
        if len(token) >= 3:
            for j in range(len(token) - 2):
                features.append(token[j : j + 3])

    for feat in features:
        h = int(hashlib.md5(feat.encode("utf-8")).hexdigest(), 16)
        dim = h % 768
        sign = 1.0 if ((h >> 10) & 1) else -1.0
        vector[dim] += sign

    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0.0:
        vector = [v / norm for v in vector]
    return vector

async def generate_embedding(text: str) -> list[float]:
    settings = get_settings()
    
    if not settings.GEMINI_API_KEY or settings.AI_PROVIDER == "mock":
        logger.warning(
            "Running in MOCK EMBEDDING mode: generating feature-hashed vocabulary embedding. "
            "Cosine similarity is approximated using token and n-gram overlap. Set GEMINI_API_KEY for deep neural embeddings."
        )
        return get_mock_embedding(text)
        
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        loop = asyncio.get_running_loop()
        
        response = await loop.run_in_executor(
            None,
            lambda: client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
        )
        return response.embeddings[0].values
    except Exception as e:
        logger.warning(f"Error generating Gemini embedding: {e}. Falling back to mock embedding.")
        return get_mock_embedding(text)

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
        
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = sum(a * a for a in v1) ** 0.5
    norm_b = sum(b * b for b in v2) ** 0.5
    
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
        
    return dot_product / (norm_a * norm_b)
