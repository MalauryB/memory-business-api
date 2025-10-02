import strawberry
from typing import Optional
from datetime import datetime
from uuid import UUID

@strawberry.type
class Address:
    street: str
    city: str
    zip_code: str
    country: str

@strawberry.input
class AddressInput:
    street: str
    city: str
    zip_code: str
    country: str

@strawberry.type
class Client:
    id: strawberry.ID
    name: str
    contact_name: str
    email: str
    phone: str
    address: Address
    created_at: datetime
    updated_at: datetime

@strawberry.input
class ClientInput:
    name: str
    contact_name: str
    email: str
    phone: str
    address: AddressInput

@strawberry.input
class UpdateClientInput:
    name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[AddressInput] = None
