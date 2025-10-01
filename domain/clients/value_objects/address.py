from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Address:
    """Value Object représentant une adresse."""

    street: str
    city: str
    zip_code: str
    country: str

    def __post_init__(self):
        """Validation du Value Object."""
        if not self.street or not self.street.strip():
            raise ValueError("Street cannot be empty")
        if not self.city or not self.city.strip():
            raise ValueError("City cannot be empty")
        if not self.zip_code or not self.zip_code.strip():
            raise ValueError("Zip code cannot be empty")
        if not self.country or not self.country.strip():
            raise ValueError("Country cannot be empty")

    def __str__(self) -> str:
        return f"{self.street}, {self.zip_code} {self.city}, {self.country}"
