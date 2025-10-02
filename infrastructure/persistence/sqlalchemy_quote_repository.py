from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.quotes.entities.quote import Quote
from domain.quotes.entities.quote_item import QuoteItem
from domain.quotes.repositories.quote_repository import QuoteRepository
from domain.quotes.value_objects.money import Money
from domain.quotes.value_objects.tax_rate import TaxRate
from infrastructure.persistence.sqlalchemy_models import QuoteModel, QuoteItemModel


class SQLAlchemyQuoteRepository(QuoteRepository):
    """Implémentation SQLAlchemy du repository Quote (Adapter)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, quote: Quote) -> Quote:
        """Sauvegarde un devis."""
        # Chercher si le devis existe déjà
        stmt = select(QuoteModel).where(QuoteModel.id == quote.id).options(selectinload(QuoteModel.items))
        result = await self.session.execute(stmt)
        db_quote = result.scalar_one_or_none()

        if db_quote:
            # Mise à jour
            db_quote.client_id = quote.client_id
            db_quote.project_id = quote.project_id
            db_quote.title = quote.title
            db_quote.status = quote.status
            db_quote.currency = quote.currency
            db_quote.total_ht = quote.total_ht.amount
            db_quote.total_ttc = quote.total_ttc.amount
            db_quote.tax_rate = quote.tax_rate.rate
            db_quote.valid_until = quote.valid_until
            db_quote.updated_at = quote.updated_at

            # Supprimer les anciens items et ajouter les nouveaux
            db_quote.items.clear()
            for item in quote.items:
                db_item = QuoteItemModel(
                    id=item.id,
                    quote_id=item.quote_id,
                    description=item.description,
                    unit_price=item.unit_price.amount,
                    quantity=item.quantity,
                    total=item.total.amount,
                    currency=item.unit_price.currency,
                )
                db_quote.items.append(db_item)
        else:
            # Création
            db_quote = QuoteModel(
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
            )

            # Ajouter les items
            for item in quote.items:
                db_item = QuoteItemModel(
                    id=item.id,
                    quote_id=item.quote_id,
                    description=item.description,
                    unit_price=item.unit_price.amount,
                    quantity=item.quantity,
                    total=item.total.amount,
                    currency=item.unit_price.currency,
                )
                db_quote.items.append(db_item)

            self.session.add(db_quote)

        await self.session.flush()
        await self.session.refresh(db_quote)
        return self._to_entity(db_quote)

    async def find_by_id(self, quote_id: UUID) -> Optional[Quote]:
        """Trouve un devis par son ID."""
        stmt = select(QuoteModel).where(QuoteModel.id == quote_id).options(selectinload(QuoteModel.items))
        result = await self.session.execute(stmt)
        db_quote = result.scalar_one_or_none()

        if db_quote:
            return self._to_entity(db_quote)
        return None

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère tous les devis avec pagination."""
        stmt = select(QuoteModel).offset(skip).limit(limit).options(selectinload(QuoteModel.items))
        result = await self.session.execute(stmt)
        db_quotes = result.scalars().all()

        return [self._to_entity(db_quote) for db_quote in db_quotes]

    async def find_by_client_id(self, client_id: UUID) -> List[Quote]:
        """Trouve tous les devis d'un client."""
        stmt = select(QuoteModel).where(QuoteModel.client_id == client_id).options(selectinload(QuoteModel.items))
        result = await self.session.execute(stmt)
        db_quotes = result.scalars().all()

        return [self._to_entity(db_quote) for db_quote in db_quotes]

    async def find_by_project_id(self, project_id: UUID) -> List[Quote]:
        """Trouve tous les devis d'un projet."""
        stmt = select(QuoteModel).where(QuoteModel.project_id == project_id).options(selectinload(QuoteModel.items))
        result = await self.session.execute(stmt)
        db_quotes = result.scalars().all()

        return [self._to_entity(db_quote) for db_quote in db_quotes]

    async def delete(self, quote_id: UUID) -> bool:
        """Supprime un devis."""
        stmt = select(QuoteModel).where(QuoteModel.id == quote_id)
        result = await self.session.execute(stmt)
        db_quote = result.scalar_one_or_none()

        if db_quote:
            await self.session.delete(db_quote)
            await self.session.flush()
            return True
        return False

    async def exists(self, quote_id: UUID) -> bool:
        """Vérifie si un devis existe."""
        stmt = select(QuoteModel.id).where(QuoteModel.id == quote_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def _to_entity(self, db_quote: QuoteModel) -> Quote:
        """Convertit un modèle SQLAlchemy en entité de domaine."""
        tax_rate = TaxRate(Decimal(str(db_quote.tax_rate)))

        # Créer les items
        items = []
        for db_item in db_quote.items:
            unit_price = Money(
                amount=Decimal(str(db_item.unit_price)),
                currency=db_item.currency
            )
            item = QuoteItem(
                id=db_item.id,
                quote_id=db_item.quote_id,
                description=db_item.description,
                unit_price=unit_price,
                quantity=Decimal(str(db_item.quantity)),
            )
            items.append(item)

        return Quote(
            id=db_quote.id,
            client_id=db_quote.client_id,
            project_id=db_quote.project_id,
            title=db_quote.title,
            status=db_quote.status,
            currency=db_quote.currency,
            tax_rate=tax_rate,
            created_at=db_quote.created_at,
            updated_at=db_quote.updated_at,
            valid_until=db_quote.valid_until,
            items=items,
        )
