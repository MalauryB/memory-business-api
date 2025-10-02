import strawberry
from typing import Optional
from datetime import datetime, date
from enum import Enum


@strawberry.enum
class ProjectStatusEnum(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@strawberry.type
class Project:
    id: strawberry.ID
    client_id: strawberry.ID
    name: str
    description: str
    status: ProjectStatusEnum
    start_date: date
    end_date: Optional[date]
    created_at: datetime
    updated_at: datetime


@strawberry.input
class ProjectInput:
    client_id: str
    name: str
    description: str
    status: ProjectStatusEnum
    start_date: date
    end_date: Optional[date] = None


@strawberry.input
class UpdateProjectInput:
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatusEnum] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
