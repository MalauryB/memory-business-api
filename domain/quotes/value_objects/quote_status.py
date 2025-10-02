from enum import Enum


class QuoteStatus(str, Enum):
    """Énumération représentant le statut d'un devis."""

    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

    def __str__(self) -> str:
        return self.value
