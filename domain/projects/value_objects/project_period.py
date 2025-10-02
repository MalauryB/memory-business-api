from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class ProjectPeriod:
    """Value Object représentant la période d'un projet."""

    start_date: date
    end_date: Optional[date] = None

    def __post_init__(self):
        """Validation du Value Object."""
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date")

    def is_ongoing(self, current_date: date) -> bool:
        """Vérifie si le projet est en cours à une date donnée."""
        if current_date < self.start_date:
            return False
        if self.end_date and current_date > self.end_date:
            return False
        return True

    def duration_days(self) -> Optional[int]:
        """Calcule la durée du projet en jours."""
        if self.end_date:
            return (self.end_date - self.start_date).days
        return None

    def __str__(self) -> str:
        if self.end_date:
            return f"{self.start_date} to {self.end_date}"
        return f"From {self.start_date}"
