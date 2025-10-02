from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.quotes.entities.quote import Quote


class QuoteRepository(ABC):
    """Interface du repository Quote (Port)."""

    @abstractmethod
    async def save(self, quote: Quote) -> Quote:
        """Sauvegarde un devis."""
        pass

    @abstractmethod
    async def find_by_id(self, quote_id: UUID) -> Optional[Quote]:
        """Trouve un devis par son ID."""
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère tous les devis avec pagination."""
        pass

    @abstractmethod
    async def find_by_client_id(self, client_id: UUID) -> List[Quote]:
        """Trouve tous les devis d'un client."""
        pass

    @abstractmethod
    async def find_by_project_id(self, project_id: UUID) -> List[Quote]:
        """Trouve tous les devis d'un projet."""
        pass

    @abstractmethod
    async def delete(self, quote_id: UUID) -> bool:
        """Supprime un devis."""
        pass

    @abstractmethod
    async def exists(self, quote_id: UUID) -> bool:
        """Vérifie si un devis existe."""
        pass
