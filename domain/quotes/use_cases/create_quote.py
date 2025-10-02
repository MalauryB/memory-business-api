from decimal import Decimal
from domain.quotes.entities.quote import Quote
from domain.quotes.entities.quote_item import QuoteItem
from domain.quotes.repositories.quote_repository import QuoteRepository
from domain.quotes.value_objects.money import Money
from domain.quotes.value_objects.tax_rate import TaxRate
from domain.quotes.dto.quote_dto import CreateQuoteDTO, QuoteResponseDTO, QuoteItemDTO


class CreateQuoteUseCase:
    """Cas d'utilisation pour créer un devis."""

    def __init__(self, quote_repository: QuoteRepository):
        self.quote_repository = quote_repository

    async def execute(self, dto: CreateQuoteDTO) -> QuoteResponseDTO:
        """Exécute le cas d'utilisation."""
        # Créer l'entité Quote via la factory method
        tax_rate = TaxRate(dto.tax_rate)
        quote = Quote.create(
            client_id=dto.client_id,
            project_id=dto.project_id,
            title=dto.title,
            currency=dto.currency,
            tax_rate=tax_rate,
            valid_until=dto.valid_until,
        )

        # Ajouter les items
        for item_dto in dto.items:
            unit_price = Money(amount=item_dto.unit_price, currency=item_dto.currency)
            item = QuoteItem.create(
                quote_id=quote.id,
                description=item_dto.description,
                unit_price=unit_price,
                quantity=item_dto.quantity,
            )
            quote.add_item(item)

        # Sauvegarder via le repository
        saved_quote = await self.quote_repository.save(quote)

        # TODO: Publier les événements de domaine
        saved_quote.clear_domain_events()

        # Mapper vers le DTO de réponse
        return self._to_response_dto(saved_quote)

    def _to_response_dto(self, quote: Quote) -> QuoteResponseDTO:
        """Convertit l'entité en DTO de réponse."""
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
