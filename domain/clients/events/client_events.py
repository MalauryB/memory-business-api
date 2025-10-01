from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent:
    """Classe de base pour les événements de domaine."""
    occurred_at: datetime


@dataclass(frozen=True)
class ClientCreated(DomainEvent):
    """Événement émis lors de la création d'un client."""
    client_id: UUID
    name: str
    email: str


@dataclass(frozen=True)
class ClientUpdated(DomainEvent):
    """Événement émis lors de la mise à jour d'un client."""
    client_id: UUID
    name: str
    email: str


@dataclass(frozen=True)
class ClientDeleted(DomainEvent):
    """Événement émis lors de la suppression d'un client."""
    client_id: UUID
