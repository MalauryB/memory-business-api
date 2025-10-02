from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class TaxRate:
    """Value Object représentant un taux de taxe (TVA)."""

    rate: Decimal

    def __post_init__(self):
        """Validation du Value Object."""
        if not isinstance(self.rate, Decimal):
            object.__setattr__(self, "rate", Decimal(str(self.rate)))

        if self.rate < 0 or self.rate > 1:
            raise ValueError("Tax rate must be between 0 and 1 (e.g., 0.20 for 20%)")

    def apply_to(self, amount: Decimal) -> Decimal:
        """Applique le taux de taxe à un montant."""
        return amount * self.rate

    def calculate_total_with_tax(self, amount_ht: Decimal) -> Decimal:
        """Calcule le montant TTC à partir du HT."""
        return amount_ht * (Decimal("1") + self.rate)

    def __str__(self) -> str:
        return f"{self.rate * 100:.1f}%"
