from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from typing import Dict
from domain.projects.value_objects.complexity import Complexity


class CreateFeatureDTO(BaseModel):
    """DTO pour créer une feature."""
    module_id: UUID = Field(..., description="Module ID")
    name: str = Field(..., min_length=1, description="Feature name")
    description: str = Field(..., min_length=1, description="Feature description")
    complexity: Complexity = Field(..., description="Feature complexity")
    profile_allocation: Dict[str, float] = Field(..., description="Profile allocation ratios")
    extra_hours: int = Field(default=0, ge=0, description="Extra hours")

    @field_validator('profile_allocation')
    @classmethod
    def validate_allocation(cls, v):
        """Valide que les ratios somment à 1.0"""
        total = sum(v.values())
        if total > 0 and abs(total - 1.0) > 0.01:
            raise ValueError(f"Profile allocation must sum to 1.0 (100%), got {total}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "module_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "User Authentication",
                "description": "Implement user login and registration",
                "complexity": "medium",
                "profile_allocation": {
                    "developer": 0.7,
                    "architect": 0.3
                },
                "extra_hours": 5
            }
        }


class UpdateFeatureDTO(BaseModel):
    """DTO pour mettre à jour une feature."""
    name: str | None = Field(None, min_length=1, description="Feature name")
    description: str | None = Field(None, min_length=1, description="Feature description")
    complexity: Complexity | None = Field(None, description="Feature complexity")
    profile_allocation: Dict[str, float] | None = Field(None, description="Profile allocation ratios")
    extra_hours: int | None = Field(None, ge=0, description="Extra hours")

    @field_validator('profile_allocation')
    @classmethod
    def validate_allocation(cls, v):
        """Valide que les ratios somment à 1.0"""
        if v is not None:
            total = sum(v.values())
            if total > 0 and abs(total - 1.0) > 0.01:
                raise ValueError(f"Profile allocation must sum to 1.0 (100%), got {total}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Advanced User Authentication",
                "complexity": "complex",
                "extra_hours": 10
            }
        }


class FeatureResponseDTO(BaseModel):
    """DTO pour la réponse feature."""
    id: UUID
    module_id: UUID
    name: str
    description: str
    complexity: Complexity
    profile_allocation: Dict[str, float]
    extra_hours: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "module_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "User Authentication",
                "description": "Implement user login and registration",
                "complexity": "medium",
                "profile_allocation": {
                    "developer": 0.7,
                    "architect": 0.3
                },
                "extra_hours": 5
            }
        }
