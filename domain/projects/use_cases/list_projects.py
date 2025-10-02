from typing import List
from domain.projects.repositories.project_repository import ProjectRepository
from domain.projects.dto.project_dto import ProjectResponseDTO


class ListProjectsUseCase:
    """Cas d'utilisation pour lister tous les projets."""

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[ProjectResponseDTO]:
        """Exécute le cas d'utilisation."""
        projects = await self.project_repository.find_all(skip=skip, limit=limit)

        return [
            ProjectResponseDTO(
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
            for project in projects
        ]
