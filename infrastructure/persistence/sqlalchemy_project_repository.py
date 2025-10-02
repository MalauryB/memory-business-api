from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.projects.entities.project import Project
from domain.projects.entities.module import Module
from domain.projects.entities.feature import Feature
from domain.projects.repositories.project_repository import ProjectRepository
from domain.projects.value_objects.project_period import ProjectPeriod
from domain.projects.value_objects.project_status import ProjectStatus
from infrastructure.persistence.sqlalchemy_models import ProjectModel, ModuleModel, FeatureModel


class SQLAlchemyProjectRepository(ProjectRepository):
    """Implémentation SQLAlchemy du repository Project (Adapter)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, project: Project) -> Project:
        """Sauvegarde un projet avec ses modules et features."""
        # Chercher si le projet existe déjà
        stmt = select(ProjectModel).options(
            selectinload(ProjectModel.modules).selectinload(ModuleModel.features)
        ).where(ProjectModel.id == project.id)
        result = await self.session.execute(stmt)
        db_project = result.scalar_one_or_none()

        if db_project:
            # Mise à jour du projet
            db_project.client_id = project.client_id
            db_project.name = project.name
            db_project.description = project.description
            db_project.status = project.status
            db_project.start_date = project.start_date
            db_project.end_date = project.end_date
            db_project.updated_at = project.updated_at

            # Synchroniser les modules
            self._sync_modules(db_project, project.modules)
        else:
            # Création
            db_project = ProjectModel(
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
            self.session.add(db_project)

            # Ajouter les modules
            for module in project.modules:
                db_module = self._module_to_model(module)
                db_project.modules.append(db_module)

        await self.session.flush()

        # Recharger avec les relations
        await self.session.refresh(db_project, ["modules"])
        return self._to_entity(db_project)

    async def find_by_id(self, project_id: UUID) -> Optional[Project]:
        """Trouve un projet par son ID avec ses modules et features."""
        stmt = select(ProjectModel).options(
            selectinload(ProjectModel.modules).selectinload(ModuleModel.features)
        ).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        db_project = result.scalar_one_or_none()

        if db_project:
            return self._to_entity(db_project)
        return None

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Récupère tous les projets avec pagination et leurs modules/features."""
        stmt = select(ProjectModel).options(
            selectinload(ProjectModel.modules).selectinload(ModuleModel.features)
        ).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        db_projects = result.scalars().all()

        return [self._to_entity(db_project) for db_project in db_projects]

    async def find_by_client_id(self, client_id: UUID) -> List[Project]:
        """Trouve tous les projets d'un client avec leurs modules/features."""
        stmt = select(ProjectModel).options(
            selectinload(ProjectModel.modules).selectinload(ModuleModel.features)
        ).where(ProjectModel.client_id == client_id)
        result = await self.session.execute(stmt)
        db_projects = result.scalars().all()

        return [self._to_entity(db_project) for db_project in db_projects]

    async def delete(self, project_id: UUID) -> bool:
        """Supprime un projet."""
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        db_project = result.scalar_one_or_none()

        if db_project:
            await self.session.delete(db_project)
            await self.session.flush()
            return True
        return False

    async def exists(self, project_id: UUID) -> bool:
        """Vérifie si un projet existe."""
        stmt = select(ProjectModel.id).where(ProjectModel.id == project_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def _to_entity(self, db_project: ProjectModel) -> Project:
        """Convertit un modèle SQLAlchemy en entité de domaine."""
        period = ProjectPeriod(
            start_date=db_project.start_date,
            end_date=db_project.end_date,
        )

        return Project(
            id=db_project.id,
            client_id=db_project.client_id,
            name=db_project.name,
            description=db_project.description,
            status=db_project.status,
            period=period,
            created_at=db_project.created_at,
            updated_at=db_project.updated_at,
        )
