from enum import Enum


class ProjectStatus(str, Enum):
    """Énumération représentant le statut d'un projet."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        return self.value
