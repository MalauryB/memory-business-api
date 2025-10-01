from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Optional
from domain.clients.value_objects.address import Address


class Client:
    """Entité Client avec logique métier."""

    def __init__(
        self,
        id: UUID,
        name: str,
        contact_name: str,
        email: str,
        phone: str,
        address: Address,
        created_at: datetime,
        updated_at: datetime,
    ):
        self._id = id
        self._name = name
        self._contact_name = contact_name
        self._email = email
        self._phone = phone
        self._address = address
        self._created_at = created_at
        self._updated_at = updated_at
        self._domain_events: List = []

        # Validation à la création
        self._validate()

    def _validate(self):
        """Valide l'entité Client."""
        if not self._name or not self._name.strip():
            raise ValueError("Client name cannot be empty")
        if not self._contact_name or not self._contact_name.strip():
            raise ValueError("Contact name cannot be empty")
        if not self._email or "@" not in self._email:
            raise ValueError("Invalid email address")
        if not self._phone or not self._phone.strip():
            raise ValueError("Phone cannot be empty")
        if not isinstance(self._address, Address):
            raise ValueError("Address must be an Address value object")

    @staticmethod
    def create(
        name: str,
        contact_name: str,
        email: str,
        phone: str,
        address: Address,
    ) -> "Client":
        """Factory method pour créer un nouveau client."""
        from domain.clients.events.client_events import ClientCreated

        now = datetime.utcnow()
        client = Client(
            id=uuid4(),
            name=name,
            contact_name=contact_name,
            email=email,
            phone=phone,
            address=address,
            created_at=now,
            updated_at=now,
        )

        # Ajouter l'événement de domaine
        client.add_domain_event(
            ClientCreated(
                client_id=client.id,
                name=client.name,
                email=client.email,
                occurred_at=now,
            )
        )

        return client

    def update(
        self,
        name: Optional[str] = None,
        contact_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[Address] = None,
    ):
        """Met à jour les informations du client."""
        from domain.clients.events.client_events import ClientUpdated

        if name is not None:
            self._name = name
        if contact_name is not None:
            self._contact_name = contact_name
        if email is not None:
            self._email = email
        if phone is not None:
            self._phone = phone
        if address is not None:
            self._address = address

        self._updated_at = datetime.utcnow()
        self._validate()

        # Ajouter l'événement de domaine
        self.add_domain_event(
            ClientUpdated(
                client_id=self.id,
                name=self.name,
                email=self.email,
                occurred_at=self._updated_at,
            )
        )

    def mark_as_deleted(self):
        """Marque le client comme supprimé."""
        from domain.clients.events.client_events import ClientDeleted

        self.add_domain_event(
            ClientDeleted(
                client_id=self.id,
                occurred_at=datetime.utcnow(),
            )
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
    def name(self) -> str:
        return self._name

    @property
    def contact_name(self) -> str:
        return self._contact_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def address(self) -> Address:
        return self._address

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def domain_events(self) -> List:
        return self._domain_events.copy()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Client):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, name='{self.name}', email='{self.email}')>"
