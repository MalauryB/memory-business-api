from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Profile:
    """Value Object représentant un profil avec son rôle et taux."""

    role: str
    tjm: Decimal  # Taux Journalier Moyen
    hourly_rate: Decimal  # Taux horaire

    def __post_init__(self):
        """Validation du Value Object."""
        if not isinstance(self.tjm, Decimal):
            object.__setattr__(self, "tjm", Decimal(str(self.tjm)))
        if not isinstance(self.hourly_rate, Decimal):
            object.__setattr__(self, "hourly_rate", Decimal(str(self.hourly_rate)))

        if not self.role or not self.role.strip():
            raise ValueError("Role cannot be empty")
        if self.tjm <= 0:
            raise ValueError("TJM must be greater than 0")
        if self.hourly_rate <= 0:
            raise ValueError("Hourly rate must be greater than 0")

    def __str__(self) -> str:
        return f"{self.role} (TJM: {self.tjm}€, Taux horaire: {self.hourly_rate}€/h)"
