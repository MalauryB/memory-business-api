from typing import List, Optional
from uuid import UUID
from infrastructure.database.session import async_session_maker
from infrastructure.persistence.sqlalchemy_project_repository import SQLAlchemyProjectRepository
from domain.projects.use_cases.create_project import CreateProjectUseCase
from domain.projects.use_cases.get_project import GetProjectUseCase
from domain.projects.use_cases.list_projects import ListProjectsUseCase
from domain.projects.use_cases.update_project import UpdateProjectUseCase
from domain.projects.use_cases.delete_project import DeleteProjectUseCase
from domain.projects.dto.project_dto import CreateProjectDTO, UpdateProjectDTO, ProjectResponseDTO
from domain.projects.value_objects.project_status import ProjectStatus
from app.schemas.project import Project, ProjectInput, UpdateProjectInput, ProjectStatusEnum


class ProjectService:
    """Service pour gérer les opérations GraphQL sur les projets."""

    async def get_all_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Récupère tous les projets."""
        async with async_session_maker() as session:
            repository = SQLAlchemyProjectRepository(session)
            use_case = ListProjectsUseCase(repository)
            projects_dto = await use_case.execute(skip=skip, limit=limit)

            return [self._dto_to_graphql(dto) for dto in projects_dto]

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Récupère un projet par son ID."""
        async with async_session_maker() as session:
            repository = SQLAlchemyProjectRepository(session)
            use_case = GetProjectUseCase(repository)

            try:
                project_dto = await use_case.execute(UUID(project_id))
                return self._dto_to_graphql(project_dto)
            except ValueError:
                return None

    async def create_project(self, project_input: ProjectInput) -> Project:
        """Crée un nouveau projet."""
        async with async_session_maker() as session:
            repository = SQLAlchemyProjectRepository(session)
            use_case = CreateProjectUseCase(repository)

            # Convertir l'input GraphQL en DTO
            create_dto = CreateProjectDTO(
                client_id=UUID(project_input.client_id),
                name=project_input.name,
                description=project_input.description,
                status=ProjectStatus(project_input.status.value),
                start_date=project_input.start_date,
                end_date=project_input.end_date,
            )

            project_dto = await use_case.execute(create_dto)
            await session.commit()

            return self._dto_to_graphql(project_dto)

    async def update_project(self, project_id: str, project_input: UpdateProjectInput) -> Optional[Project]:
        """Met à jour un projet."""
        async with async_session_maker() as session:
            repository = SQLAlchemyProjectRepository(session)
            use_case = UpdateProjectUseCase(repository)

            # Convertir l'input GraphQL en DTO
            update_dto = UpdateProjectDTO(
                name=project_input.name,
                description=project_input.description,
                status=ProjectStatus(project_input.status.value) if project_input.status else None,
                start_date=project_input.start_date,
                end_date=project_input.end_date,
            )

            try:
                project_dto = await use_case.execute(UUID(project_id), update_dto)
                await session.commit()
                return self._dto_to_graphql(project_dto)
            except ValueError:
                return None

    async def delete_project(self, project_id: str) -> bool:
        """Supprime un projet."""
        async with async_session_maker() as session:
            repository = SQLAlchemyProjectRepository(session)
            use_case = DeleteProjectUseCase(repository)

            try:
                await use_case.execute(UUID(project_id))
                await session.commit()
                return True
            except ValueError:
                return False

    def _dto_to_graphql(self, dto: ProjectResponseDTO) -> Project:
        """Convertit un DTO en type GraphQL."""
        return Project(
            id=str(dto.id),
            client_id=str(dto.client_id),
            name=dto.name,
            description=dto.description,
            status=ProjectStatusEnum(dto.status.value),
            start_date=dto.start_date,
            end_date=dto.end_date,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
