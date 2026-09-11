from abc import ABC, abstractmethod

class StorageProvider(ABC):

    @abstractmethod
    async def save(self, filename: str, content: bytes) -> str:
        ...

    @abstractmethod
    def get_url(self, filename: str) -> str:
        ...
