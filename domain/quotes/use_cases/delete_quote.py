from uuid import UUID
from domain.quotes.repositories.quote_repository import QuoteRepository


class DeleteQuoteUseCase:
    """Cas d'utilisation pour supprimer un devis."""

    def __init__(self, quote_repository: QuoteRepository):
        self.quote_repository = quote_repository

    async def execute(self, quote_id: UUID) -> None:
        """Exécute le cas d'utilisation."""
        quote = await self.quote_repository.find_by_id(quote_id)

        if not quote:
            raise ValueError(f"Quote with ID {quote_id} not found")

        # Marquer comme supprimé (événement de domaine)
        quote.mark_as_deleted()

        # TODO: Publier les événements de domaine

        # Supprimer du repository
        await self.quote_repository.delete(quote_id)
