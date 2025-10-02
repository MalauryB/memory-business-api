from uuid import UUID
from domain.quotes.repositories.quote_repository import QuoteRepository
from domain.quotes.dto.quote_dto import QuoteResponseDTO, QuoteItemDTO
from domain.quotes.value_objects.quote_status import QuoteStatus


class ChangeQuoteStatusUseCase:
    """Cas d'utilisation pour changer le statut d'un devis."""

    def __init__(self, quote_repository: QuoteRepository):
        self.quote_repository = quote_repository

    async def execute(self, quote_id: UUID, new_status: QuoteStatus) -> QuoteResponseDTO:
        """Exécute le cas d'utilisation."""
        quote = await self.quote_repository.find_by_id(quote_id)

        if not quote:
            raise ValueError(f"Quote with ID {quote_id} not found")

        # Appliquer le changement de statut
        if new_status == QuoteStatus.SENT:
            quote.send()
        elif new_status == QuoteStatus.ACCEPTED:
            quote.accept()
        elif new_status == QuoteStatus.REJECTED:
            quote.reject()
        elif new_status == QuoteStatus.EXPIRED:
            quote.mark_as_expired()

        # Sauvegarder
        saved_quote = await self.quote_repository.save(quote)

        # TODO: Publier les événements de domaine
        saved_quote.clear_domain_events()

        # Mapper vers le DTO de réponse
        items_dto = [
            QuoteItemDTO(
                id=item.id,
                quote_id=item.quote_id,
                description=item.description,
                unit_price=item.unit_price.amount,
                quantity=item.quantity,
                total=item.total.amount,
                currency=item.unit_price.currency,
            )
            for item in saved_quote.items
        ]

        return QuoteResponseDTO(
            id=saved_quote.id,
            client_id=saved_quote.client_id,
            project_id=saved_quote.project_id,
            title=saved_quote.title,
            status=saved_quote.status,
            currency=saved_quote.currency,
            total_ht=saved_quote.total_ht.amount,
            total_ttc=saved_quote.total_ttc.amount,
            tax_rate=saved_quote.tax_rate.rate,
            created_at=saved_quote.created_at,
            updated_at=saved_quote.updated_at,
            valid_until=saved_quote.valid_until,
            items=items_dto,
        )
