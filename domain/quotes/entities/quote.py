from datetime import datetime, date
from uuid import UUID, uuid4
from typing import List, Optional
from decimal import Decimal
from domain.quotes.value_objects.quote_status import QuoteStatus
from domain.quotes.value_objects.money import Money
from domain.quotes.value_objects.tax_rate import TaxRate
from domain.quotes.entities.quote_item import QuoteItem


class Quote:
    """Entité Quote avec logique métier."""

    def __init__(
        self,
        id: UUID,
        client_id: UUID,
        title: str,
        status: QuoteStatus,
        currency: str,
        tax_rate: TaxRate,
        created_at: datetime,
        updated_at: datetime,
        valid_until: date,
        project_id: Optional[UUID] = None,
        items: Optional[List[QuoteItem]] = None,
    ):
        self._id = id
        self._client_id = client_id
        self._project_id = project_id
        self._title = title
        self._status = status
        self._currency = currency
        self._tax_rate = tax_rate
        self._created_at = created_at
        self._updated_at = updated_at
        self._valid_until = valid_until
        self._items: List[QuoteItem] = items or []
        self._domain_events: List = []

        self._validate()

    def _validate(self):
        """Valide l'entité Quote."""
        if not self._title or not self._title.strip():
            raise ValueError("Quote title cannot be empty")
        if not isinstance(self._status, QuoteStatus):
            raise ValueError("Invalid quote status")
        if not isinstance(self._tax_rate, TaxRate):
            raise ValueError("Tax rate must be a TaxRate value object")
        if self._valid_until < self._created_at.date():
            raise ValueError("Valid until date cannot be before creation date")

    @staticmethod
    def create(
        client_id: UUID,
        title: str,
        currency: str = "EUR",
        tax_rate: TaxRate = None,
        valid_until: date = None,
        project_id: Optional[UUID] = None,
    ) -> "Quote":
        """Factory method pour créer un nouveau devis."""
        from domain.quotes.events.quote_events import QuoteCreated

        now = datetime.utcnow()
        tax_rate = tax_rate or TaxRate(Decimal("0.20"))  # 20% par défaut
        valid_until = valid_until or date.today().replace(day=date.today().day + 30)

        quote = Quote(
            id=uuid4(),
            client_id=client_id,
            project_id=project_id,
            title=title,
            status=QuoteStatus.DRAFT,
            currency=currency,
            tax_rate=tax_rate,
            created_at=now,
            updated_at=now,
            valid_until=valid_until,
        )

        quote.add_domain_event(
            QuoteCreated(
                quote_id=quote.id,
                client_id=quote.client_id,
                title=quote.title,
                occurred_at=now,
            )
        )

        return quote

    def add_item(self, item: QuoteItem):
        """Ajoute un item au devis."""
        if item.quote_id != self.id:
            raise ValueError("Item does not belong to this quote")
        self._items.append(item)
        self._updated_at = datetime.utcnow()

    def remove_item(self, item_id: UUID):
        """Supprime un item du devis."""
        self._items = [item for item in self._items if item.id != item_id]
        self._updated_at = datetime.utcnow()

    def update(
        self,
        title: Optional[str] = None,
        valid_until: Optional[date] = None,
        project_id: Optional[UUID] = None,
    ):
        """Met à jour les informations du devis."""
        from domain.quotes.events.quote_events import QuoteUpdated

        if title is not None:
            self._title = title
        if valid_until is not None:
            self._valid_until = valid_until
        if project_id is not None:
            self._project_id = project_id

        self._updated_at = datetime.utcnow()
        self._validate()

        self.add_domain_event(
            QuoteUpdated(
                quote_id=self.id,
                title=self.title,
                status=self.status,
                occurred_at=self._updated_at,
            )
        )

    def send(self):
        """Marque le devis comme envoyé."""
        from domain.quotes.events.quote_events import QuoteSent

        if self._status != QuoteStatus.DRAFT:
            raise ValueError("Only draft quotes can be sent")

        self._status = QuoteStatus.SENT
        self._updated_at = datetime.utcnow()

        self.add_domain_event(
            QuoteSent(
                quote_id=self.id,
                occurred_at=self._updated_at,
            )
        )

    def accept(self):
        """Marque le devis comme accepté."""
        from domain.quotes.events.quote_events import QuoteAccepted

        if self._status != QuoteStatus.SENT:
            raise ValueError("Only sent quotes can be accepted")

        self._status = QuoteStatus.ACCEPTED
        self._updated_at = datetime.utcnow()

        self.add_domain_event(
            QuoteAccepted(
                quote_id=self.id,
                occurred_at=self._updated_at,
            )
        )

    def reject(self):
        """Marque le devis comme rejeté."""
        from domain.quotes.events.quote_events import QuoteRejected

        if self._status != QuoteStatus.SENT:
            raise ValueError("Only sent quotes can be rejected")

        self._status = QuoteStatus.REJECTED
        self._updated_at = datetime.utcnow()

        self.add_domain_event(
            QuoteRejected(
                quote_id=self.id,
                occurred_at=self._updated_at,
            )
        )

    def mark_as_expired(self):
        """Marque le devis comme expiré."""
        from domain.quotes.events.quote_events import QuoteExpired

        self._status = QuoteStatus.EXPIRED
        self._updated_at = datetime.utcnow()

        self.add_domain_event(
            QuoteExpired(
                quote_id=self.id,
                occurred_at=self._updated_at,
            )
        )

    def mark_as_deleted(self):
        """Marque le devis comme supprimé."""
        from domain.quotes.events.quote_events import QuoteDeleted

        self.add_domain_event(
            QuoteDeleted(
                quote_id=self.id,
                occurred_at=datetime.utcnow(),
            )
        )

    def calculate_total_ht(self) -> Money:
        """Calcule le total HT du devis."""
        total = Decimal("0")
        for item in self._items:
            total += item.total.amount
        return Money(amount=total, currency=self._currency)

    def calculate_total_ttc(self) -> Money:
        """Calcule le total TTC du devis."""
        total_ht = self.calculate_total_ht()
        total_ttc_amount = self._tax_rate.calculate_total_with_tax(total_ht.amount)
        return Money(amount=total_ttc_amount, currency=self._currency)

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
    def project_id(self) -> Optional[UUID]:
        return self._project_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def status(self) -> QuoteStatus:
        return self._status

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def tax_rate(self) -> TaxRate:
        return self._tax_rate

    @property
    def total_ht(self) -> Money:
        return self.calculate_total_ht()

    @property
    def total_ttc(self) -> Money:
        return self.calculate_total_ttc()

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def valid_until(self) -> date:
        return self._valid_until

    @property
    def items(self) -> List[QuoteItem]:
        return self._items.copy()

    @property
    def domain_events(self) -> List:
        return self._domain_events.copy()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quote):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Quote(id={self.id}, title='{self.title}', status='{self.status}')>"
