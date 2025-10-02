from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from domain.quotes.value_objects.quote_status import QuoteStatus


class QuoteItemDTO(BaseModel):
    """DTO pour un item de devis."""
    id: UUID
    quote_id: UUID
    description: str
    unit_price: Decimal
    quantity: Decimal
    total: Decimal
    currency: str = "EUR"

    class Config:
        from_attributes = True


class CreateQuoteItemDTO(BaseModel):
    """DTO pour créer un item de devis."""
    description: str = Field(..., min_length=1, description="Item description")
    unit_price: Decimal = Field(..., gt=0, description="Unit price")
    quantity: Decimal = Field(..., gt=0, description="Quantity")
    currency: str = Field(default="EUR", description="Currency code")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Website development",
                "unit_price": 1500.00,
                "quantity": 10,
                "currency": "EUR"
            }
        }


class CreateQuoteDTO(BaseModel):
    """DTO pour créer un devis."""
    client_id: UUID = Field(..., description="Client ID")
    project_id: Optional[UUID] = Field(None, description="Project ID (optional)")
    title: str = Field(..., min_length=1, description="Quote title")
    currency: str = Field(default="EUR", description="Currency code")
    tax_rate: Decimal = Field(default=Decimal("0.20"), ge=0, le=1, description="Tax rate (0-1)")
    valid_until: date = Field(..., description="Quote validity date")
    items: List[CreateQuoteItemDTO] = Field(default_factory=list, description="Quote items")

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Website Development Quote",
                "currency": "EUR",
                "tax_rate": 0.20,
                "valid_until": "2024-03-31",
                "items": [
                    {
                        "description": "Frontend development",
                        "unit_price": 1500.00,
                        "quantity": 10,
                        "currency": "EUR"
                    }
                ]
            }
        }


class UpdateQuoteDTO(BaseModel):
    """DTO pour mettre à jour un devis."""
    title: Optional[str] = Field(None, min_length=1, description="Quote title")
    valid_until: Optional[date] = Field(None, description="Quote validity date")
    project_id: Optional[UUID] = Field(None, description="Project ID")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Website Development Quote V2",
                "valid_until": "2024-04-30"
            }
        }


class AddQuoteItemDTO(BaseModel):
    """DTO pour ajouter un item à un devis."""
    description: str = Field(..., min_length=1, description="Item description")
    unit_price: Decimal = Field(..., gt=0, description="Unit price")
    quantity: Decimal = Field(..., gt=0, description="Quantity")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Backend development",
                "unit_price": 2000.00,
                "quantity": 15
            }
        }


class QuoteResponseDTO(BaseModel):
    """DTO pour la réponse devis."""
    id: UUID
    client_id: UUID
    project_id: Optional[UUID]
    title: str
    status: QuoteStatus
    currency: str
    total_ht: Decimal
    total_ttc: Decimal
    tax_rate: Decimal
    created_at: datetime
    updated_at: datetime
    valid_until: date
    items: List[QuoteItemDTO] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "client_id": "123e4567-e89b-12d3-a456-426614174001",
                "project_id": "123e4567-e89b-12d3-a456-426614174002",
                "title": "Website Development Quote",
                "status": "draft",
                "currency": "EUR",
                "total_ht": 15000.00,
                "total_ttc": 18000.00,
                "tax_rate": 0.20,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
                "valid_until": "2024-03-31",
                "items": []
            }
        }
