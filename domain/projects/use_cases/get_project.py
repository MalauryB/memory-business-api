from uuid import UUID
from domain.projects.repositories.project_repository import ProjectRepository
from domain.projects.dto.project_dto import ProjectResponseDTO


class GetProjectUseCase:
    """Cas d'utilisation pour récupérer un projet par son ID."""

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, project_id: UUID) -> ProjectResponseDTO:
        """Exécute le cas d'utilisation."""
        project = await self.project_repository.find_by_id(project_id)

        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        return ProjectResponseDTO(
            id=project.id,
            client_id=project.client_id,
            name=project.name,
            description=project.description,
            status=project.status,
            start_date=project.start_date,
            end_date=project.end_date,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
