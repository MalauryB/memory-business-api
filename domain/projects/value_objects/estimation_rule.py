from dataclasses import dataclass
from domain.projects.value_objects.complexity import Complexity


@dataclass(frozen=True)
class EstimationRule:
    """Value Object représentant une règle d'estimation."""

    complexity: Complexity
    average_hours: float

    def __post_init__(self):
        """Validation du Value Object."""
        if self.average_hours <= 0:
            raise ValueError("Average hours must be greater than 0")

    def __str__(self) -> str:
        return f"{self.complexity}: {self.average_hours}h"
