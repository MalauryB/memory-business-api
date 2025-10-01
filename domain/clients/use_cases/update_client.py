from uuid import UUID
from domain.clients.entities.client import Client
from domain.clients.repositories.client_repository import ClientRepository
from domain.clients.value_objects.address import Address
from domain.clients.dto.client_dto import UpdateClientDTO, ClientResponseDTO, AddressDTO


class UpdateClientUseCase:
    """Cas d'utilisation pour mettre à jour un client."""

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    async def execute(self, client_id: UUID, dto: UpdateClientDTO) -> ClientResponseDTO:
        """Exécute le cas d'utilisation."""

        # Récupérer le client existant
        client = await self.client_repository.find_by_id(client_id)
        if not client:
            raise ValueError(f"Client with id {client_id} not found")

        # Si l'email est modifié, vérifier qu'il n'existe pas déjà
        if dto.email and dto.email != client.email:
            existing_client = await self.client_repository.find_by_email(dto.email)
            if existing_client:
                raise ValueError(f"Client with email {dto.email} already exists")

        # Créer le nouveau value object Address si fourni
        address = None
        if dto.address:
            address = Address(
                street=dto.address.street,
                city=dto.address.city,
                zip_code=dto.address.zip_code,
                country=dto.address.country,
            )

        # Mettre à jour l'entité
        client.update(
            name=dto.name,
            contact_name=dto.contact_name,
            email=dto.email,
            phone=dto.phone,
            address=address,
        )

        # Sauvegarder via le repository
        updated_client = await self.client_repository.save(client)

        # TODO: Publier les événements de domaine
        # event_publisher.publish(updated_client.domain_events)
        updated_client.clear_domain_events()

        # Mapper vers le DTO de réponse
        return self._to_response_dto(updated_client)

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
