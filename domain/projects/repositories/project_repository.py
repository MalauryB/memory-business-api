from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.projects.entities.project import Project


class ProjectRepository(ABC):
    """Interface du repository Project (Port)."""

    @abstractmethod
    async def save(self, project: Project) -> Project:
        """Sauvegarde un projet."""
        pass

    @abstractmethod
    async def find_by_id(self, project_id: UUID) -> Optional[Project]:
        """Trouve un projet par son ID."""
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Récupère tous les projets avec pagination."""
        pass

    @abstractmethod
    async def find_by_client_id(self, client_id: UUID) -> List[Project]:
        """Trouve tous les projets d'un client."""
        pass

    @abstractmethod
    async def delete(self, project_id: UUID) -> bool:
        """Supprime un projet."""
        pass

    @abstractmethod
    async def exists(self, project_id: UUID) -> bool:
        """Vérifie si un projet existe."""
        pass
