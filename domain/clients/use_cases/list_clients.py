from typing import List
from domain.clients.entities.client import Client
from domain.clients.repositories.client_repository import ClientRepository
from domain.clients.dto.client_dto import ClientResponseDTO, AddressDTO


class ListClientsUseCase:
    """Cas d'utilisation pour lister les clients."""

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[ClientResponseDTO]:
        """Exécute le cas d'utilisation."""

        clients = await self.client_repository.find_all(skip=skip, limit=limit)

        return [self._to_response_dto(client) for client in clients]

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
