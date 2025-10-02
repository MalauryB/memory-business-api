from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OverheadPercentage:
    """Value Object représentant un pourcentage de frais généraux."""

    type: str
    rate: Decimal

    def __post_init__(self):
        """Validation du Value Object."""
        if not isinstance(self.rate, Decimal):
            object.__setattr__(self, "rate", Decimal(str(self.rate)))

        if not self.type or not self.type.strip():
            raise ValueError("Type cannot be empty")
        if self.rate < 0 or self.rate > 1:
            raise ValueError("Rate must be between 0 and 1")

    def apply_to(self, amount: Decimal) -> Decimal:
        """Applique le pourcentage à un montant."""
        return amount * self.rate

    def __str__(self) -> str:
        return f"{self.type}: {self.rate * 100:.1f}%"
