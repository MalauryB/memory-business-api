from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from domain.projects.value_objects.project_status import ProjectStatus


@dataclass(frozen=True)
class DomainEvent:
    """Classe de base pour les événements de domaine."""
    occurred_at: datetime


@dataclass(frozen=True)
class ProjectCreated(DomainEvent):
    """Événement émis lors de la création d'un projet."""
    project_id: UUID
    client_id: UUID
    name: str
    status: ProjectStatus


@dataclass(frozen=True)
class ProjectUpdated(DomainEvent):
    """Événement émis lors de la mise à jour d'un projet."""
    project_id: UUID
    name: str
    status: ProjectStatus


@dataclass(frozen=True)
class ProjectCompleted(DomainEvent):
    """Événement émis lorsqu'un projet est complété."""
    project_id: UUID


@dataclass(frozen=True)
class ProjectDeleted(DomainEvent):
    """Événement émis lors de la suppression d'un projet."""
    project_id: UUID
