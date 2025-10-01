from uuid import UUID
from domain.clients.entities.client import Client
from domain.clients.repositories.client_repository import ClientRepository
from domain.clients.dto.client_dto import ClientResponseDTO, AddressDTO


class GetClientUseCase:
    """Cas d'utilisation pour récupérer un client par son ID."""

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    async def execute(self, client_id: UUID) -> ClientResponseDTO:
        """Exécute le cas d'utilisation."""

        client = await self.client_repository.find_by_id(client_id)

        if not client:
            raise ValueError(f"Client with id {client_id} not found")

        return self._to_response_dto(client)

    def _to_response_dto(self, client: Client) -> ClientResponseDTO:
        """Convertit l'entité en DTO de réponse."""
        return ClientResponseDTO(
            id=client.id,
            name=client.name,
            contact_name=client.contact_name,
            email=client.email,
            phone=client.phone,
            address=AddressDTO(
                street=client.address.street,
                city=client.address.city,
                zip_code=client.address.zip_code,
                country=client.address.country,
            ),
            created_at=client.created_at,
            updated_at=client.updated_at,
        )
