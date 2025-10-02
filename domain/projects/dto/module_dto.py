from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional
from domain.projects.dto.feature_dto import FeatureResponseDTO


class CreateModuleDTO(BaseModel):
    """DTO pour créer un module."""
    project_id: UUID = Field(..., description="Project ID")
    name: str = Field(..., min_length=1, description="Module name")

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Authentication Module"
            }
        }


class UpdateModuleDTO(BaseModel):
    """DTO pour mettre à jour un module."""
    name: str | None = Field(None, min_length=1, description="Module name")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Advanced Authentication Module"
            }
        }


class ModuleResponseDTO(BaseModel):
    """DTO pour la réponse module."""
    id: UUID
    project_id: UUID
    name: str
    features: Optional[List[FeatureResponseDTO]] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "project_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Authentication Module",
                "features": []
            }
        }
