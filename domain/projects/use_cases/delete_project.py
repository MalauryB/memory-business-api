from uuid import UUID
from domain.projects.repositories.project_repository import ProjectRepository


class DeleteProjectUseCase:
    """Cas d'utilisation pour supprimer un projet."""

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def execute(self, project_id: UUID) -> None:
        """Exécute le cas d'utilisation."""
        project = await self.project_repository.find_by_id(project_id)

        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        # Marquer comme supprimé (événement de domaine)
        project.mark_as_deleted()

        # TODO: Publier les événements de domaine
        # event_publisher.publish(project.domain_events)

        # Supprimer du repository
        await self.project_repository.delete(project_id)
