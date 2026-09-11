from typing import AsyncGenerator
import uuid
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Query, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import get_settings
from app.core.database import async_session_factory
from app.models.user import User
from app.core.security import decode_access_token
from app.ai.base import AIProvider
from app.ai.mock_provider import MockProvider
from app.ai.gemini_provider import GeminiProvider
from app.ai.groq_provider import GroqProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.fallback_provider import FallbackAIProvider
from app.ai.local_provider import LocalPyTorchProvider
from app.storage.base import StorageProvider
from app.storage.local_storage import LocalStorage

logger = logging.getLogger(__name__)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

def _build_provider(provider_name: str) -> AIProvider:
    settings = get_settings()

    if provider_name == "gemini":
        if not settings.GEMINI_API_KEY:
            logger.warning(
                "GEMINI_API_KEY is not set but AI_PROVIDER=gemini. Falling back to MockProvider."
            )
            return MockProvider()
        primary = GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL,
        )
        return FallbackAIProvider(primary, MockProvider())

    if provider_name == "groq":
        if not settings.GROQ_API_KEY:
            logger.warning(
                "GROQ_API_KEY is not set but AI_PROVIDER=groq. Falling back to MockProvider."
            )
            return MockProvider()
        primary = GroqProvider(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
        )
        return FallbackAIProvider(primary, MockProvider())

    if provider_name == "openai":
        if not settings.OPENAI_API_KEY:
            logger.warning(
                "OPENAI_API_KEY is not set but AI_PROVIDER=openai. Falling back to MockProvider."
            )
            return MockProvider()
        primary = OpenAIProvider(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
        )
        return FallbackAIProvider(primary, MockProvider())

    if provider_name == "local":
        return FallbackAIProvider(LocalPyTorchProvider(), MockProvider())

    return MockProvider()

def get_ai_provider() -> AIProvider:
    settings = get_settings()
    return _build_provider(settings.AI_PROVIDER)

def get_ai_provider_by_name(provider_name: str) -> AIProvider:
    valid = {"mock", "gemini", "groq", "openai", "local"}
    if provider_name not in valid:
        logger.warning(f"Unknown AI provider '{provider_name}', falling back to default.")
        return get_ai_provider()
    return _build_provider(provider_name)

def get_storage_provider() -> StorageProvider:
    settings = get_settings()
    return LocalStorage(upload_dir=settings.UPLOAD_DIR)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

async def get_current_user(
    token_bearer: str | None = Depends(oauth2_scheme),
    token_query: str | None = Query(None, alias="token"),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = token_bearer or token_query
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided."
        )
        
    if token.lower().startswith("bearer "):
        token = token[7:]
        
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature has expired or is invalid."
        )
        
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing subject identity."
        )
        
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token subject identity."
        )
        
    result = await db.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with this token does not exist."
        )
        
    return user

async def get_current_farmer(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in {"FARMER", "AGRONOMIST", "ADMIN"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to Farmers."
        )
    return current_user

async def get_current_agronomist(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in {"AGRONOMIST", "ADMIN"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation restricted to Agronomists and Admins."
        )
    return current_user

