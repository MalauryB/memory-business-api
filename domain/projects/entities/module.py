from uuid import UUID, uuid4
from typing import List, Optional
from decimal import Decimal
from domain.projects.entities.feature import Feature
from domain.projects.value_objects.estimation_rule import EstimationRule
from domain.projects.value_objects.profile import Profile


class Module:
    """Entité Module représentant un module d'un projet."""

    def __init__(
        self,
        id: UUID,
        project_id: UUID,
        name: str,
        features: Optional[List[Feature]] = None,
    ):
        self._id = id
        self._project_id = project_id
        self._name = name
        self._features: List[Feature] = features or []

        self._validate()

    def _validate(self):
        """Valide l'entité Module."""
        if not self._name or not self._name.strip():
            raise ValueError("Module name cannot be empty")

    @staticmethod
    def create(
        project_id: UUID,
        name: str,
    ) -> "Module":
        """Factory method pour créer un nouveau module."""
        return Module(
            id=uuid4(),
            project_id=project_id,
            name=name,
        )

    def add_feature(self, feature: Feature):
        """Ajoute une feature au module."""
        if feature.module_id != self.id:
            raise ValueError("Feature does not belong to this module")
        self._features.append(feature)

    def remove_feature(self, feature_id: UUID):
        """Supprime une feature du module."""
        self._features = [f for f in self._features if f.id != feature_id]

    def update(self, name: str = None):
        """Met à jour le module."""
        if name is not None:
            self._name = name
        self._validate()

    def calculate_total_hours(
        self,
        estimation_rules: List[EstimationRule]
    ) -> float:
        """Calcule le total des heures estimées pour toutes les features."""
        # Créer un dictionnaire des règles par complexité
        rules_by_complexity = {rule.complexity: rule for rule in estimation_rules}

        total_hours = 0.0
        for feature in self._features:
            if feature.complexity not in rules_by_complexity:
                raise ValueError(f"No estimation rule found for complexity {feature.complexity}")

            rule = rules_by_complexity[feature.complexity]
            total_hours += feature.calculate_estimated_hours(rule)

        return total_hours

    def calculate_total_cost(
        self,
        estimation_rules: List[EstimationRule],
        profiles: List[Profile]
    ) -> Decimal:
        """Calcule le coût total estimé pour toutes les features."""
        # Créer un dictionnaire des règles par complexité
        rules_by_complexity = {rule.complexity: rule for rule in estimation_rules}

        total_cost = Decimal("0")
        for feature in self._features:
            if feature.complexity not in rules_by_complexity:
                raise ValueError(f"No estimation rule found for complexity {feature.complexity}")

            rule = rules_by_complexity[feature.complexity]
            total_cost += feature.calculate_estimated_cost(rule, profiles)

        return total_cost

    # Properties (getters)
    @property
    def id(self) -> UUID:
        return self._id

    @property
    def project_id(self) -> UUID:
        return self._project_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def features(self) -> List[Feature]:
        return self._features.copy()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Module):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Module(id={self.id}, name='{self.name}', features_count={len(self._features)})>"
