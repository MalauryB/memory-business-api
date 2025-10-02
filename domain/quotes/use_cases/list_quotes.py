from typing import List
from domain.quotes.repositories.quote_repository import QuoteRepository
from domain.quotes.dto.quote_dto import QuoteResponseDTO, QuoteItemDTO


class ListQuotesUseCase:
    """Cas d'utilisation pour lister tous les devis."""

    def __init__(self, quote_repository: QuoteRepository):
        self.quote_repository = quote_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[QuoteResponseDTO]:
        """Exécute le cas d'utilisation."""
        quotes = await self.quote_repository.find_all(skip=skip, limit=limit)

        return [self._to_response_dto(quote) for quote in quotes]

    def _to_response_dto(self, quote) -> QuoteResponseDTO:
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
            for item in quote.items
        ]

        return QuoteResponseDTO(
            id=quote.id,
            client_id=quote.client_id,
            project_id=quote.project_id,
            title=quote.title,
            status=quote.status,
            currency=quote.currency,
            total_ht=quote.total_ht.amount,
            total_ttc=quote.total_ttc.amount,
            tax_rate=quote.tax_rate.rate,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
            valid_until=quote.valid_until,
            items=items_dto,
        )
