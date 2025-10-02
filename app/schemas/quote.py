import strawberry
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


@strawberry.enum
class QuoteStatusEnum(Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


@strawberry.type
class QuoteItem:
    id: strawberry.ID
    quote_id: strawberry.ID
    description: str
    unit_price: Decimal
    quantity: Decimal
    total: Decimal
    currency: str


@strawberry.input
class QuoteItemInput:
    description: str
    unit_price: Decimal
    quantity: Decimal
    currency: str = "EUR"


@strawberry.type
class Quote:
    id: strawberry.ID
    client_id: strawberry.ID
    project_id: Optional[strawberry.ID]
    title: str
    status: QuoteStatusEnum
    currency: str
    total_ht: Decimal
    total_ttc: Decimal
    tax_rate: Decimal
    created_at: datetime
    updated_at: datetime
    valid_until: date
    items: List[QuoteItem]


@strawberry.input
class QuoteInput:
    client_id: str
    project_id: Optional[str] = None
    title: str
    currency: str = "EUR"
    tax_rate: Decimal = Decimal("0.20")
    valid_until: date
    items: List[QuoteItemInput] = strawberry.field(default_factory=list)


@strawberry.input
class AddQuoteItemInput:
    description: str
    unit_price: Decimal
    quantity: Decimal
