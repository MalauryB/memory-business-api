from enum import Enum


class Complexity(str, Enum):
    """Énumération représentant la complexité d'une feature."""

    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"

    def __str__(self) -> str:
        return self.value
