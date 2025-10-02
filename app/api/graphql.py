import strawberry
from typing import List, Optional
from app.schemas.client import Client, ClientInput, UpdateClientInput
from app.services.client_service import ClientService

client_service = ClientService()

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL!"

    @strawberry.field
    async def clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return await client_service.get_all_clients(skip=skip, limit=limit)

    @strawberry.field
    async def client(self, id: str) -> Optional[Client]:
        return await client_service.get_client_by_id(id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_client(self, client_input: ClientInput) -> Client:
        return await client_service.create_client(client_input)

    @strawberry.mutation
    async def update_client(self, id: str, client_input: UpdateClientInput) -> Optional[Client]:
        return await client_service.update_client(id, client_input)

    @strawberry.mutation
    async def delete_client(self, id: str) -> bool:
        return await client_service.delete_client(id)

schema = strawberry.Schema(query=Query, mutation=Mutation)
