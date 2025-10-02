from uuid import UUID, uuid4
from decimal import Decimal
from domain.quotes.value_objects.money import Money


class QuoteItem:
    """Entité QuoteItem représentant une ligne de devis."""

    def __init__(
        self,
        id: UUID,
        quote_id: UUID,
        description: str,
        unit_price: Money,
        quantity: Decimal,
    ):
        self._id = id
        self._quote_id = quote_id
        self._description = description
        self._unit_price = unit_price
        self._quantity = quantity

        self._validate()

    def _validate(self):
        """Valide l'entité QuoteItem."""
        if not self._description or not self._description.strip():
            raise ValueError("Description cannot be empty")
        if not isinstance(self._unit_price, Money):
            raise ValueError("Unit price must be a Money value object")
        if self._quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

    @staticmethod
    def create(
        quote_id: UUID,
        description: str,
        unit_price: Money,
        quantity: Decimal,
    ) -> "QuoteItem":
        """Factory method pour créer un nouvel item de devis."""
        return QuoteItem(
            id=uuid4(),
            quote_id=quote_id,
            description=description,
            unit_price=unit_price,
            quantity=quantity,
        )

    def update(
        self,
        description: str = None,
        unit_price: Money = None,
        quantity: Decimal = None,
    ):
        """Met à jour l'item."""
        if description is not None:
            self._description = description
        if unit_price is not None:
            self._unit_price = unit_price
        if quantity is not None:
            self._quantity = quantity
        self._validate()

    def calculate_total(self) -> Money:
        """Calcule le total de la ligne (prix unitaire × quantité)."""
        return self._unit_price.multiply(self._quantity)

    # Properties (getters)
    @property
    def id(self) -> UUID:
        return self._id

    @property
    def quote_id(self) -> UUID:
        return self._quote_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def unit_price(self) -> Money:
        return self._unit_price

    @property
    def quantity(self) -> Decimal:
        return self._quantity

    @property
    def total(self) -> Money:
        return self.calculate_total()

    def __eq__(self, other) -> bool:
        if not isinstance(other, QuoteItem):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<QuoteItem(id={self.id}, description='{self.description}', total={self.total})>"
