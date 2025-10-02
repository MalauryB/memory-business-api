from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Dict


@dataclass(frozen=True)
class ProjectEstimation:
    """Value Object représentant l'estimation d'un projet."""

    total_hours: float
    total_cost: Decimal
    details: Optional[Dict] = None

    def __post_init__(self):
        """Validation du Value Object."""
        if not isinstance(self.total_cost, Decimal):
            object.__setattr__(self, "total_cost", Decimal(str(self.total_cost)))

        if self.total_hours < 0:
            raise ValueError("Total hours cannot be negative")
        if self.total_cost < 0:
            raise ValueError("Total cost cannot be negative")

    def __str__(self) -> str:
        return f"{self.total_hours}h pour {self.total_cost}€"
