from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.clients.entities.client import Client
from domain.clients.repositories.client_repository import ClientRepository
from domain.clients.value_objects.address import Address
from infrastructure.persistence.sqlalchemy_models import ClientModel


class SQLAlchemyClientRepository(ClientRepository):
    """Implémentation SQLAlchemy du repository Client (Adapter)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, client: Client) -> Client:
        """Sauvegarde un client."""
        # Chercher si le client existe déjà
        stmt = select(ClientModel).where(ClientModel.id == client.id)
        result = await self.session.execute(stmt)
        db_client = result.scalar_one_or_none()

        if db_client:
            # Mise à jour
            db_client.name = client.name
            db_client.contact_name = client.contact_name
            db_client.email = client.email
            db_client.phone = client.phone
            db_client.address_street = client.address.street
            db_client.address_city = client.address.city
            db_client.address_zip_code = client.address.zip_code
            db_client.address_country = client.address.country
            db_client.updated_at = client.updated_at
        else:
            # Création
            db_client = ClientModel(
                id=client.id,
                name=client.name,
                contact_name=client.contact_name,
                email=client.email,
                phone=client.phone,
                address_street=client.address.street,
                address_city=client.address.city,
                address_zip_code=client.address.zip_code,
                address_country=client.address.country,
                created_at=client.created_at,
                updated_at=client.updated_at,
            )
            self.session.add(db_client)

        await self.session.flush()
        return self._to_entity(db_client)

    async def find_by_id(self, client_id: UUID) -> Optional[Client]:
        """Trouve un client par son ID."""
        stmt = select(ClientModel).where(ClientModel.id == client_id)
        result = await self.session.execute(stmt)
        db_client = result.scalar_one_or_none()

        if db_client:
            return self._to_entity(db_client)
        return None

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """Récupère tous les clients avec pagination."""
        stmt = select(ClientModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        db_clients = result.scalars().all()

        return [self._to_entity(db_client) for db_client in db_clients]

    async def find_by_email(self, email: str) -> Optional[Client]:
        """Trouve un client par son email."""
        stmt = select(ClientModel).where(ClientModel.email == email)
        result = await self.session.execute(stmt)
        db_client = result.scalar_one_or_none()

        if db_client:
            return self._to_entity(db_client)
        return None

    async def delete(self, client_id: UUID) -> bool:
        """Supprime un client."""
        stmt = select(ClientModel).where(ClientModel.id == client_id)
        result = await self.session.execute(stmt)
        db_client = result.scalar_one_or_none()

        if db_client:
            await self.session.delete(db_client)
            await self.session.flush()
            return True
        return False

    async def exists(self, client_id: UUID) -> bool:
        """Vérifie si un client existe."""
        stmt = select(ClientModel.id).where(ClientModel.id == client_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def _to_entity(self, db_client: ClientModel) -> Client:
        """Convertit un modèle SQLAlchemy en entité de domaine."""
        address = Address(
            street=db_client.address_street,
            city=db_client.address_city,
            zip_code=db_client.address_zip_code,
            country=db_client.address_country,
        )

        return Client(
            id=db_client.id,
            name=db_client.name,
            contact_name=db_client.contact_name,
            email=db_client.email,
            phone=db_client.phone,
            address=address,
            created_at=db_client.created_at,
            updated_at=db_client.updated_at,
        )
