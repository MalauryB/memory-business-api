from uuid import UUID
from domain.projects.repositories.project_repository import ProjectRepository
from domain.projects.dto.project_dto import UpdateProjectDTO, ProjectResponseDTO


class UpdateProjectUseCase:
    """Cas d'utilisation pour mettre à jour un projet."""

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, project_id: UUID, dto: UpdateProjectDTO) -> ProjectResponseDTO:
        """Exécute le cas d'utilisation."""
        project = await self.project_repository.find_by_id(project_id)

        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        # Mettre à jour l'entité
        project.update(
            name=dto.name,
            description=dto.description,
            status=dto.status,
            start_date=dto.start_date,
            end_date=dto.end_date,
        )

        # Sauvegarder
        saved_project = await self.project_repository.save(project)

        # TODO: Publier les événements de domaine
        # event_publisher.publish(saved_project.domain_events)
        saved_project.clear_domain_events()

        return ProjectResponseDTO(
            id=saved_project.id,
            client_id=saved_project.client_id,
            name=saved_project.name,
            description=saved_project.description,
            status=saved_project.status,
            start_date=saved_project.start_date,
            end_date=saved_project.end_date,
            created_at=saved_project.created_at,
            updated_at=saved_project.updated_at,
        )
