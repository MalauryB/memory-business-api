from datetime import datetime, date
from uuid import UUID, uuid4
from typing import List, Optional, TYPE_CHECKING
from decimal import Decimal
from domain.projects.value_objects.project_status import ProjectStatus
from domain.projects.value_objects.project_period import ProjectPeriod
from domain.projects.value_objects.project_estimation import ProjectEstimation
from domain.projects.value_objects.estimation_rule import EstimationRule
from domain.projects.value_objects.profile import Profile
from domain.projects.value_objects.overhead_percentage import OverheadPercentage

if TYPE_CHECKING:
    from domain.projects.entities.module import Module


class Project:
    """Entité Project avec logique métier."""

    def __init__(
        self,
        id: UUID,
        client_id: UUID,
        name: str,
        description: str,
        status: ProjectStatus,
        period: ProjectPeriod,
        created_at: datetime,
        updated_at: datetime,
        modules: Optional[List["Module"]] = None,
    ):
        self._id = id
        self._client_id = client_id
        self._name = name
        self._description = description
        self._status = status
        self._period = period
        self._created_at = created_at
        self._updated_at = updated_at
        self._modules: List["Module"] = modules or []
        self._domain_events: List = []

        # Validation à la création
        self._validate()

    def _validate(self):
        """Valide l'entité Project."""
        if not self._name or not self._name.strip():
            raise ValueError("Project name cannot be empty")
        if not self._description or not self._description.strip():
            raise ValueError("Project description cannot be empty")
        if not isinstance(self._status, ProjectStatus):
            raise ValueError("Invalid project status")
        if not isinstance(self._period, ProjectPeriod):
            raise ValueError("Period must be a ProjectPeriod value object")

    @staticmethod
    def create(
        client_id: UUID,
        name: str,
        description: str,
        start_date: date,
        end_date: Optional[date] = None,
        status: ProjectStatus = ProjectStatus.PLANNED,
    ) -> "Project":
        """Factory method pour créer un nouveau projet."""
        from domain.projects.events.project_events import ProjectCreated

        now = datetime.utcnow()
        period = ProjectPeriod(start_date=start_date, end_date=end_date)

        project = Project(
            id=uuid4(),
            client_id=client_id,
            name=name,
            description=description,
            status=status,
            period=period,
            created_at=now,
            updated_at=now,
        )

        # Ajouter l'événement de domaine
        project.add_domain_event(
            ProjectCreated(
                project_id=project.id,
                client_id=project.client_id,
                name=project.name,
                status=project.status,
                occurred_at=now,
            )
        )

        return project

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[ProjectStatus] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        """Met à jour les informations du projet."""
        from domain.projects.events.project_events import ProjectUpdated

        if name is not None:
            self._name = name
        if description is not None:
            self._description = description
        if status is not None:
            self._status = status
        if start_date is not None or end_date is not None:
            new_start = start_date if start_date is not None else self._period.start_date
            new_end = end_date if end_date is not None else self._period.end_date
            self._period = ProjectPeriod(start_date=new_start, end_date=new_end)

        self._updated_at = datetime.utcnow()
        self._validate()

        # Ajouter l'événement de domaine
        self.add_domain_event(
            ProjectUpdated(
                project_id=self.id,
                name=self.name,
                status=self.status,
                occurred_at=self._updated_at,
            )
        )

    def complete(self):
        """Marque le projet comme complété."""
        from domain.projects.events.project_events import ProjectCompleted

        self._status = ProjectStatus.COMPLETED
        self._updated_at = datetime.utcnow()

        self.add_domain_event(
            ProjectCompleted(
                project_id=self.id,
                occurred_at=self._updated_at,
            )
        )

    def mark_as_deleted(self):
        """Marque le projet comme supprimé."""
        from domain.projects.events.project_events import ProjectDeleted

        self.add_domain_event(
            ProjectDeleted(
                project_id=self.id,
                occurred_at=datetime.utcnow(),
            )
        )

    def add_module(self, module: "Module"):
        """Ajoute un module au projet."""
        if module.project_id != self.id:
            raise ValueError("Module does not belong to this project")
        self._modules.append(module)

    def remove_module(self, module_id: UUID):
        """Supprime un module du projet."""
        self._modules = [m for m in self._modules if m.id != module_id]

    def calculate_estimation(
        self,
        estimation_rules: List[EstimationRule],
        profiles: List[Profile],
        overhead_percentages: Optional[List[OverheadPercentage]] = None
    ) -> ProjectEstimation:
        """Calcule l'estimation totale du projet avec tous ses modules."""
        total_hours = 0.0
        total_cost = Decimal("0")

        # Calculer les heures et coûts de tous les modules
        for module in self._modules:
            total_hours += module.calculate_total_hours(estimation_rules)
            total_cost += module.calculate_total_cost(estimation_rules, profiles)

        # Appliquer les frais généraux
        if overhead_percentages:
            for overhead in overhead_percentages:
                total_cost += overhead.apply_to(total_cost)

        details = {
            "modules_count": len(self._modules),
            "total_features": sum(len(m.features) for m in self._modules)
        }

        return ProjectEstimation(
            total_hours=total_hours,
            total_cost=total_cost,
            details=details
        )

    def add_domain_event(self, event):
        """Ajoute un événement de domaine."""
        self._domain_events.append(event)

    def clear_domain_events(self):
        """Nettoie les événements de domaine."""
        self._domain_events.clear()

    # Properties (getters)
    @property
    def id(self) -> UUID:
        return self._id

    @property
    def client_id(self) -> UUID:
        return self._client_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> ProjectStatus:
        return self._status

    @property
    def period(self) -> ProjectPeriod:
        return self._period

    @property
    def start_date(self) -> date:
        return self._period.start_date

    @property
    def end_date(self) -> Optional[date]:
        return self._period.end_date

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def domain_events(self) -> List:
        return self._domain_events.copy()

    @property
    def modules(self) -> List["Module"]:
        return self._modules.copy()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Project):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
