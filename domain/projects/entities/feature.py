from uuid import UUID, uuid4
from typing import Dict, List
from decimal import Decimal
from domain.projects.value_objects.complexity import Complexity
from domain.projects.value_objects.profile import Profile
from domain.projects.value_objects.estimation_rule import EstimationRule


class Feature:
    """Entité Feature représentant une fonctionnalité d'un module."""

    def __init__(
        self,
        id: UUID,
        module_id: UUID,
        name: str,
        description: str,
        complexity: Complexity,
        profile_allocation: Dict[str, float],
        extra_hours: int = 0,
    ):
        self._id = id
        self._module_id = module_id
        self._name = name
        self._description = description
        self._complexity = complexity
        self._profile_allocation = profile_allocation
        self._extra_hours = extra_hours

        self._validate()

    def _validate(self):
        """Valide l'entité Feature."""
        if not self._name or not self._name.strip():
            raise ValueError("Feature name cannot be empty")
        if not isinstance(self._complexity, Complexity):
            raise ValueError("Invalid complexity")
        if self._extra_hours < 0:
            raise ValueError("Extra hours cannot be negative")

        # Valider que les ratios d'allocation somment à 1 (100%)
        total_ratio = sum(self._profile_allocation.values())
        if total_ratio > 0 and abs(total_ratio - 1.0) > 0.01:  # Tolérance de 1%
            raise ValueError(f"Profile allocation must sum to 1.0 (100%), got {total_ratio}")

    @staticmethod
    def create(
        module_id: UUID,
        name: str,
        description: str,
        complexity: Complexity,
        profile_allocation: Dict[str, float],
        extra_hours: int = 0,
    ) -> "Feature":
        """Factory method pour créer une nouvelle feature."""
        return Feature(
            id=uuid4(),
            module_id=module_id,
            name=name,
            description=description,
            complexity=complexity,
            profile_allocation=profile_allocation,
            extra_hours=extra_hours,
        )

    def update(
        self,
        name: str = None,
        description: str = None,
        complexity: Complexity = None,
        profile_allocation: Dict[str, float] = None,
        extra_hours: int = None,
    ):
        """Met à jour la feature."""
        if name is not None:
            self._name = name
        if description is not None:
            self._description = description
        if complexity is not None:
            self._complexity = complexity
        if profile_allocation is not None:
            self._profile_allocation = profile_allocation
        if extra_hours is not None:
            self._extra_hours = extra_hours
        self._validate()

    def calculate_estimated_hours(self, estimation_rule: EstimationRule) -> float:
        """Calcule les heures estimées basées sur la règle d'estimation."""
        if estimation_rule.complexity != self._complexity:
            raise ValueError(f"Estimation rule complexity {estimation_rule.complexity} doesn't match feature complexity {self._complexity}")

        return estimation_rule.average_hours + self._extra_hours

    def calculate_estimated_cost(
        self,
        estimation_rule: EstimationRule,
        profiles: List[Profile]
    ) -> Decimal:
        """Calcule le coût estimé basé sur les profils et leur allocation."""
        total_hours = self.calculate_estimated_hours(estimation_rule)
        total_cost = Decimal("0")

        # Créer un dictionnaire des profils par rôle
        profile_by_role = {profile.role: profile for profile in profiles}

        for role, ratio in self._profile_allocation.items():
            if role not in profile_by_role:
                raise ValueError(f"Profile {role} not found in available profiles")

            profile = profile_by_role[role]
            hours_for_profile = total_hours * ratio
            cost_for_profile = Decimal(str(hours_for_profile)) * profile.hourly_rate
            total_cost += cost_for_profile

        return total_cost

    # Properties (getters)
    @property
    def id(self) -> UUID:
        return self._id

    @property
    def module_id(self) -> UUID:
        return self._module_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def complexity(self) -> Complexity:
        return self._complexity

    @property
    def profile_allocation(self) -> Dict[str, float]:
        return self._profile_allocation.copy()

    @property
    def extra_hours(self) -> int:
        return self._extra_hours

    def __eq__(self, other) -> bool:
        if not isinstance(other, Feature):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Feature(id={self.id}, name='{self.name}', complexity='{self.complexity}')>"
