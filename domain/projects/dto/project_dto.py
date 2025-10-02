from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from domain.projects.value_objects.project_status import ProjectStatus


class CreateProjectDTO(BaseModel):
    """DTO pour créer un projet."""
    client_id: UUID = Field(..., description="Client ID")
    name: str = Field(..., min_length=1, description="Project name")
    description: str = Field(..., min_length=1, description="Project description")
    status: ProjectStatus = Field(default=ProjectStatus.PLANNED, description="Project status")
    start_date: date = Field(..., description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Website Redesign",
                "description": "Complete redesign of company website",
                "status": "planned",
                "start_date": "2024-02-01",
                "end_date": "2024-06-30"
            }
        }


class UpdateProjectDTO(BaseModel):
    """DTO pour mettre à jour un projet."""
    name: Optional[str] = Field(None, min_length=1, description="Project name")
    description: Optional[str] = Field(None, min_length=1, description="Project description")
    status: Optional[ProjectStatus] = Field(None, description="Project status")
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Website Redesign V2",
                "status": "in_progress",
                "end_date": "2024-08-31"
            }
        }


class ProjectEstimationResponseDTO(BaseModel):
    """DTO pour la réponse d'estimation."""
    total_hours: float
    total_cost: Decimal
    details: Optional[dict] = None

    class Config:
        from_attributes = True


class ProjectResponseDTO(BaseModel):
    """DTO pour la réponse projet."""
    id: UUID
    client_id: UUID
    name: str
    description: str
    status: ProjectStatus
    start_date: date
    end_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    modules: Optional[List["ModuleResponseDTO"]] = []
    estimation: Optional[ProjectEstimationResponseDTO] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "client_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Website Redesign",
                "description": "Complete redesign of company website",
                "status": "in_progress",
                "start_date": "2024-02-01",
                "end_date": "2024-06-30",
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
                "modules": [],
                "estimation": None
            }
        }


# Import après la définition pour éviter les imports circulaires
from domain.projects.dto.module_dto import ModuleResponseDTO
ProjectResponseDTO.model_rebuild()
