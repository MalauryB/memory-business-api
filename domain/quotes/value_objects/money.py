from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """Value Object représentant une somme d'argent."""

    amount: Decimal
    currency: str = "EUR"

    def __post_init__(self):
        """Validation du Value Object."""
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))

        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a 3-letter code (e.g., EUR, USD)")

    def add(self, other: "Money") -> "Money":
        """Additionne deux montants."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def multiply(self, factor: Decimal) -> "Money":
        """Multiplie le montant par un facteur."""
        return Money(amount=self.amount * factor, currency=self.currency)

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"
