import secrets
from pathlib import Path

import aiofiles

from app.storage.base import StorageProvider

class LocalStorage(StorageProvider):

    def __init__(self, upload_dir: str = "uploads"):
        self._upload_dir = Path(upload_dir)
        self._upload_dir.mkdir(parents=True, exist_ok=True)

    def _generate_secure_filename(self, original_filename: str) -> str:
        ext = Path(original_filename).suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp"):
            ext = ".jpg"
        return f"{secrets.token_hex(16)}{ext}"

    async def save(self, filename: str, content: bytes) -> str:
        secure_name = self._generate_secure_filename(filename)
        filepath = self._upload_dir / secure_name

        async with aiofiles.open(filepath, "wb") as f:
            await f.write(content)

        return secure_name

    def get_url(self, filename: str) -> str:
        return f"/uploads/{filename}"
