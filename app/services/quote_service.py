from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from infrastructure.database.session import async_session_maker
from infrastructure.persistence.sqlalchemy_quote_repository import SQLAlchemyQuoteRepository
from domain.quotes.use_cases.create_quote import CreateQuoteUseCase
from domain.quotes.use_cases.get_quote import GetQuoteUseCase
from domain.quotes.use_cases.list_quotes import ListQuotesUseCase
from domain.quotes.use_cases.add_quote_item import AddQuoteItemUseCase
from domain.quotes.use_cases.change_quote_status import ChangeQuoteStatusUseCase
from domain.quotes.use_cases.delete_quote import DeleteQuoteUseCase
from domain.quotes.dto.quote_dto import CreateQuoteDTO, QuoteResponseDTO, AddQuoteItemDTO, CreateQuoteItemDTO
from domain.quotes.value_objects.quote_status import QuoteStatus
from app.schemas.quote import Quote, QuoteInput, AddQuoteItemInput, QuoteItem, QuoteStatusEnum


class QuoteService:
    """Service pour gérer les opérations GraphQL sur les devis."""

    async def get_all_quotes(self, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère tous les devis."""
        async with async_session_maker() as session:
            repository = SQLAlchemyQuoteRepository(session)
            use_case = ListQuotesUseCase(repository)
            quotes_dto = await use_case.execute(skip=skip, limit=limit)

            return [self._dto_to_graphql(dto) for dto in quotes_dto]

    async def get_quote_by_id(self, quote_id: str) -> Optional[Quote]:
        """Récupère un devis par son ID."""
        async with async_session_maker() as session:
            repository = SQLAlchemyQuoteRepository(session)
            use_case = GetQuoteUseCase(repository)

            try:
                quote_dto = await use_case.execute(UUID(quote_id))
                return self._dto_to_graphql(quote_dto)
            except ValueError:
                return None

    async def create_quote(self, quote_input: QuoteInput) -> Quote:
        """Crée un nouveau devis."""
        async with async_session_maker() as session:
            repository = SQLAlchemyQuoteRepository(session)
            use_case = CreateQuoteUseCase(repository)

            # Convertir l'input GraphQL en DTO
            items_dto = [
                CreateQuoteItemDTO(
                    description=item.description,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                    currency=item.currency,
                )
                for item in quote_input.items
            ]

            create_dto = CreateQuoteDTO(
                client_id=UUID(quote_input.client_id),
                project_id=UUID(quote_input.project_id) if quote_input.project_id else None,
                title=quote_input.title,
                currency=quote_input.currency,
                tax_rate=quote_input.tax_rate,
                valid_until=quote_input.valid_until,
                items=items_dto,
            )

            quote_dto = await use_case.execute(create_dto)
            await session.commit()

            return self._dto_to_graphql(quote_dto)

    async def add_item_to_quote(self, quote_id: str, item_input: AddQuoteItemInput) -> Optional[Quote]:
        """Ajoute un item à un devis."""
        async with async_session_maker() as session:
            repository = SQLAlchemyQuoteRepository(session)
            use_case = AddQuoteItemUseCase(repository)

            add_item_dto = AddQuoteItemDTO(
                description=item_input.description,
                unit_price=item_input.unit_price,
                quantity=item_input.quantity,
            )

            try:
                quote_dto = await use_case.execute(UUID(quote_id), add_item_dto)
                await session.commit()
                return self._dto_to_graphql(quote_dto)
            except ValueError:
                return None

    async def change_quote_status(self, quote_id: str, new_status: QuoteStatusEnum) -> Optional[Quote]:
        """Change le statut d'un devis."""
        async with async_session_maker() as session:
            repository = SQLAlchemyQuoteRepository(session)
            use_case = ChangeQuoteStatusUseCase(repository)

            try:
                quote_dto = await use_case.execute(UUID(quote_id), QuoteStatus(new_status.value))
                await session.commit()
                return self._dto_to_graphql(quote_dto)
            except ValueError:
                return None

    async def delete_quote(self, quote_id: str) -> bool:
        """Supprime un devis."""
        async with async_session_maker() as session:
            repository = SQLAlchemyQuoteRepository(session)
            use_case = DeleteQuoteUseCase(repository)

            try:
                await use_case.execute(UUID(quote_id))
                await session.commit()
                return True
            except ValueError:
                return False

    def _dto_to_graphql(self, dto: QuoteResponseDTO) -> Quote:
        """Convertit un DTO en type GraphQL."""
        items = [
            QuoteItem(
                id=str(item.id),
                quote_id=str(item.quote_id),
                description=item.description,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total=item.total,
                currency=item.currency,
            )
            for item in dto.items
        ]

        return Quote(
            id=str(dto.id),
            client_id=str(dto.client_id),
            project_id=str(dto.project_id) if dto.project_id else None,
            title=dto.title,
            status=QuoteStatusEnum(dto.status.value),
            currency=dto.currency,
            total_ht=dto.total_ht,
            total_ttc=dto.total_ttc,
            tax_rate=dto.tax_rate,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            valid_until=dto.valid_until,
            items=items,
        )
