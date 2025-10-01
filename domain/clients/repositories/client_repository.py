from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.clients.entities.client import Client


class ClientRepository(ABC):
    """Interface du repository Client (Port)."""

    @abstractmethod
    async def save(self, client: Client) -> Client:
        """Sauvegarde un client."""
        pass

    @abstractmethod
    async def find_by_id(self, client_id: UUID) -> Optional[Client]:
        """Trouve un client par son ID."""
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """Récupère tous les clients avec pagination."""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Client]:
        """Trouve un client par son email."""
        pass

    @abstractmethod
    async def delete(self, client_id: UUID) -> bool:
        """Supprime un client."""
        pass

    @abstractmethod
    async def exists(self, client_id: UUID) -> bool:
        """Vérifie si un client existe."""
        pass
