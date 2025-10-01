from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AddressDTO(BaseModel):
    """DTO pour l'adresse."""
    street: str = Field(..., min_length=1, description="Street address")
    city: str = Field(..., min_length=1, description="City")
    zip_code: str = Field(..., min_length=1, description="Zip code")
    country: str = Field(..., min_length=1, description="Country")

    class Config:
        json_schema_extra = {
            "example": {
                "street": "123 Main St",
                "city": "Paris",
                "zip_code": "75001",
                "country": "France"
            }
        }


class CreateClientDTO(BaseModel):
    """DTO pour créer un client."""
    name: str = Field(..., min_length=1, description="Client name")
    contact_name: str = Field(..., min_length=1, description="Contact person name")
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., min_length=1, description="Phone number")
    address: AddressDTO = Field(..., description="Client address")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Acme Corp",
                "contact_name": "John Doe",
                "email": "john@acme.com",
                "phone": "+33 1 23 45 67 89",
                "address": {
                    "street": "123 Main St",
                    "city": "Paris",
                    "zip_code": "75001",
                    "country": "France"
                }
            }
        }


class UpdateClientDTO(BaseModel):
    """DTO pour mettre à jour un client."""
    name: Optional[str] = Field(None, min_length=1, description="Client name")
    contact_name: Optional[str] = Field(None, min_length=1, description="Contact person name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, min_length=1, description="Phone number")
    address: Optional[AddressDTO] = Field(None, description="Client address")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Acme Corp Updated",
                "contact_name": "Jane Doe",
                "email": "jane@acme.com",
                "phone": "+33 1 23 45 67 90",
                "address": {
                    "street": "456 New St",
                    "city": "Lyon",
                    "zip_code": "69001",
                    "country": "France"
                }
            }
        }


class ClientResponseDTO(BaseModel):
    """DTO pour la réponse client."""
    id: UUID
    name: str
    contact_name: str
    email: str
    phone: str
    address: AddressDTO
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Acme Corp",
                "contact_name": "John Doe",
                "email": "john@acme.com",
                "phone": "+33 1 23 45 67 89",
                "address": {
                    "street": "123 Main St",
                    "city": "Paris",
                    "zip_code": "75001",
                    "country": "France"
                },
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
