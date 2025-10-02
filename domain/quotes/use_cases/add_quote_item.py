from uuid import UUID
from domain.quotes.entities.quote_item import QuoteItem
from domain.quotes.repositories.quote_repository import QuoteRepository
from domain.quotes.value_objects.money import Money
from domain.quotes.dto.quote_dto import AddQuoteItemDTO, QuoteResponseDTO, QuoteItemDTO


class AddQuoteItemUseCase:
    """Cas d'utilisation pour ajouter un item à un devis."""

    def __init__(self, quote_repository: QuoteRepository):
        self.quote_repository = quote_repository

    async def execute(self, quote_id: UUID, dto: AddQuoteItemDTO) -> QuoteResponseDTO:
        """Exécute le cas d'utilisation."""
        quote = await self.quote_repository.find_by_id(quote_id)

        if not quote:
            raise ValueError(f"Quote with ID {quote_id} not found")

        # Créer le nouvel item
        unit_price = Money(amount=dto.unit_price, currency=quote.currency)
        item = QuoteItem.create(
            quote_id=quote.id,
            description=dto.description,
            unit_price=unit_price,
            quantity=dto.quantity,
        )

        # Ajouter l'item au devis
        quote.add_item(item)

        # Sauvegarder
        saved_quote = await self.quote_repository.save(quote)

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
