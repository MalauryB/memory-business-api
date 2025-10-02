from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from domain.quotes.value_objects.quote_status import QuoteStatus


@dataclass(frozen=True)
class DomainEvent:
    """Classe de base pour les événements de domaine."""
    occurred_at: datetime


@dataclass(frozen=True)
class QuoteCreated(DomainEvent):
    """Événement émis lors de la création d'un devis."""
    quote_id: UUID
    client_id: UUID
    title: str


@dataclass(frozen=True)
class QuoteUpdated(DomainEvent):
    """Événement émis lors de la mise à jour d'un devis."""
    quote_id: UUID
    title: str
    status: QuoteStatus


@dataclass(frozen=True)
class QuoteSent(DomainEvent):
    """Événement émis lorsqu'un devis est envoyé."""
    quote_id: UUID


@dataclass(frozen=True)
class QuoteAccepted(DomainEvent):
    """Événement émis lorsqu'un devis est accepté."""
    quote_id: UUID


@dataclass(frozen=True)
class QuoteRejected(DomainEvent):
    """Événement émis lorsqu'un devis est rejeté."""
    quote_id: UUID


@dataclass(frozen=True)
class QuoteExpired(DomainEvent):
    """Événement émis lorsqu'un devis est expiré."""
    quote_id: UUID


@dataclass(frozen=True)
class QuoteDeleted(DomainEvent):
    """Événement émis lors de la suppression d'un devis."""
    quote_id: UUID
