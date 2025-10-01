import strawberry
from typing import Optional

@strawberry.type
class User:
    id: int
    name: str
    email: str
    age: Optional[int] = None

@strawberry.input
class UserInput:
    name: str
    email: str
    age: Optional[int] = None
