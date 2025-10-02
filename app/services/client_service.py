from typing import List, Optional
from uuid import UUID
from infrastructure.database.session import async_session_maker
from infrastructure.persistence.sqlalchemy_client_repository import SQLAlchemyClientRepository
from domain.clients.use_cases.create_client import CreateClientUseCase
from domain.clients.use_cases.get_client import GetClientUseCase
from domain.clients.use_cases.list_clients import ListClientsUseCase
from domain.clients.use_cases.update_client import UpdateClientUseCase
from domain.clients.use_cases.delete_client import DeleteClientUseCase
from domain.clients.dto.client_dto import CreateClientDTO, UpdateClientDTO, ClientResponseDTO, AddressDTO
from app.schemas.client import Client, ClientInput, UpdateClientInput, Address


class ClientService:
    """Service pour gérer les opérations GraphQL sur les clients."""

    async def get_all_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """Récupère tous les clients."""
        async with async_session_maker() as session:
            repository = SQLAlchemyClientRepository(session)
            use_case = ListClientsUseCase(repository)
            clients_dto = await use_case.execute(skip=skip, limit=limit)

            return [self._dto_to_graphql(dto) for dto in clients_dto]

    async def get_client_by_id(self, client_id: str) -> Optional[Client]:
        """Récupère un client par son ID."""
        async with async_session_maker() as session:
            repository = SQLAlchemyClientRepository(session)
            use_case = GetClientUseCase(repository)

            try:
                client_dto = await use_case.execute(UUID(client_id))
                return self._dto_to_graphql(client_dto)
            except ValueError:
                return None

    async def create_client(self, client_input: ClientInput) -> Client:
        """Crée un nouveau client."""
        async with async_session_maker() as session:
            repository = SQLAlchemyClientRepository(session)
            use_case = CreateClientUseCase(repository)

            # Convertir l'input GraphQL en DTO
            create_dto = CreateClientDTO(
                name=client_input.name,
                contact_name=client_input.contact_name,
                email=client_input.email,
                phone=client_input.phone,
                address=AddressDTO(
                    street=client_input.address.street,
                    city=client_input.address.city,
                    zip_code=client_input.address.zip_code,
                    country=client_input.address.country,
                )
            )

            client_dto = await use_case.execute(create_dto)
            await session.commit()

            return self._dto_to_graphql(client_dto)

    async def update_client(self, client_id: str, client_input: UpdateClientInput) -> Optional[Client]:
        """Met à jour un client."""
        async with async_session_maker() as session:
            repository = SQLAlchemyClientRepository(session)
            use_case = UpdateClientUseCase(repository)

            # Convertir l'input GraphQL en DTO
            address_dto = None
            if client_input.address:
                address_dto = AddressDTO(
                    street=client_input.address.street,
                    city=client_input.address.city,
                    zip_code=client_input.address.zip_code,
                    country=client_input.address.country,
                )

            update_dto = UpdateClientDTO(
                name=client_input.name,
                contact_name=client_input.contact_name,
                email=client_input.email,
                phone=client_input.phone,
                address=address_dto,
            )

            try:
                client_dto = await use_case.execute(UUID(client_id), update_dto)
                await session.commit()
                return self._dto_to_graphql(client_dto)
            except ValueError:
                return None

    async def delete_client(self, client_id: str) -> bool:
        """Supprime un client."""
        async with async_session_maker() as session:
            repository = SQLAlchemyClientRepository(session)
            use_case = DeleteClientUseCase(repository)

            try:
                await use_case.execute(UUID(client_id))
                await session.commit()
                return True
            except ValueError:
                return False

    def _dto_to_graphql(self, dto: ClientResponseDTO) -> Client:
        """Convertit un DTO en type GraphQL."""
        return Client(
            id=str(dto.id),
            name=dto.name,
            contact_name=dto.contact_name,
            email=dto.email,
            phone=dto.phone,
            address=Address(
                street=dto.address.street,
                city=dto.address.city,
                zip_code=dto.address.zip_code,
                country=dto.address.country,
            ),
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
