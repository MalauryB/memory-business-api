from uuid import UUID
from domain.clients.repositories.client_repository import ClientRepository


class DeleteClientUseCase:
    """Cas d'utilisation pour supprimer un client."""

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    async def execute(self, client_id: UUID) -> bool:
        """Exécute le cas d'utilisation."""

        # Vérifier si le client existe
        client = await self.client_repository.find_by_id(client_id)
        if not client:
            raise ValueError(f"Client with id {client_id} not found")

        # Marquer comme supprimé (événement de domaine)
        client.mark_as_deleted()

        # TODO: Publier les événements de domaine
        # event_publisher.publish(client.domain_events)
        client.clear_domain_events()

        # Supprimer via le repository
        return await self.client_repository.delete(client_id)
