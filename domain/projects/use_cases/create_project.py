from domain.projects.entities.project import Project
from domain.projects.repositories.project_repository import ProjectRepository
from domain.projects.dto.project_dto import CreateProjectDTO, ProjectResponseDTO


class CreateProjectUseCase:
    """Cas d'utilisation pour créer un projet."""

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, dto: CreateProjectDTO) -> ProjectResponseDTO:
        """Exécute le cas d'utilisation."""

        # Créer l'entité Project via la factory method
        project = Project.create(
            client_id=dto.client_id,
            name=dto.name,
            description=dto.description,
            start_date=dto.start_date,
            end_date=dto.end_date,
            status=dto.status,
        )

        # Sauvegarder via le repository
        saved_project = await self.project_repository.save(project)

        # TODO: Publier les événements de domaine
        # event_publisher.publish(saved_project.domain_events)
        saved_project.clear_domain_events()

        # Mapper vers le DTO de réponse
        return self._to_response_dto(saved_project)

    def _to_response_dto(self, project: Project) -> ProjectResponseDTO:
        """Convertit l'entité en DTO de réponse."""
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
