from domain.clients.entities.client import Client
from domain.clients.repositories.client_repository import ClientRepository
from domain.clients.value_objects.address import Address
from domain.clients.dto.client_dto import CreateClientDTO, ClientResponseDTO


class CreateClientUseCase:
    """Cas d'utilisation pour créer un client."""

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    async def execute(self, dto: CreateClientDTO) -> ClientResponseDTO:
        """Exécute le cas d'utilisation."""

        # Vérifier si l'email existe déjà
        existing_client = await self.client_repository.find_by_email(dto.email)
        if existing_client:
            raise ValueError(f"Client with email {dto.email} already exists")

        # Créer le value object Address
        address = Address(
            street=dto.address.street,
            city=dto.address.city,
            zip_code=dto.address.zip_code,
            country=dto.address.country,
        )

        # Créer l'entité Client via la factory method
        client = Client.create(
            name=dto.name,
            contact_name=dto.contact_name,
            email=dto.email,
            phone=dto.phone,
            address=address,
        )

        # Sauvegarder via le repository
        saved_client = await self.client_repository.save(client)

        # TODO: Publier les événements de domaine
        # event_publisher.publish(saved_client.domain_events)
        saved_client.clear_domain_events()

        # Mapper vers le DTO de réponse
        return self._to_response_dto(saved_client)

    def _to_response_dto(self, client: Client) -> ClientResponseDTO:
        """Convertit l'entité en DTO de réponse."""
        from domain.clients.dto.client_dto import AddressDTO

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
