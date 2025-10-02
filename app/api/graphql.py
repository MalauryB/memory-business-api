import strawberry
from typing import List, Optional
from app.schemas.client import Client, ClientInput, UpdateClientInput
from app.schemas.project import Project, ProjectInput, UpdateProjectInput
from app.schemas.quote import Quote, QuoteInput, AddQuoteItemInput, QuoteStatusEnum
from app.services.client_service import ClientService
from app.services.project_service import ProjectService
from app.services.quote_service import QuoteService

client_service = ClientService()
project_service = ProjectService()
quote_service = QuoteService()

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

    @strawberry.field
    async def projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return await project_service.get_all_projects(skip=skip, limit=limit)

    @strawberry.field
    async def project(self, id: str) -> Optional[Project]:
        return await project_service.get_project_by_id(id)

    @strawberry.field
    async def quotes(self, skip: int = 0, limit: int = 100) -> List[Quote]:
        return await quote_service.get_all_quotes(skip=skip, limit=limit)

    @strawberry.field
    async def quote(self, id: str) -> Optional[Quote]:
        return await quote_service.get_quote_by_id(id)

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

    @strawberry.mutation
    async def create_project(self, project_input: ProjectInput) -> Project:
        return await project_service.create_project(project_input)

    @strawberry.mutation
    async def update_project(self, id: str, project_input: UpdateProjectInput) -> Optional[Project]:
        return await project_service.update_project(id, project_input)

    @strawberry.mutation
    async def delete_project(self, id: str) -> bool:
        return await project_service.delete_project(id)

    @strawberry.mutation
    async def create_quote(self, quote_input: QuoteInput) -> Quote:
        return await quote_service.create_quote(quote_input)

    @strawberry.mutation
    async def add_quote_item(self, quote_id: str, item_input: AddQuoteItemInput) -> Optional[Quote]:
        return await quote_service.add_item_to_quote(quote_id, item_input)

    @strawberry.mutation
    async def change_quote_status(self, quote_id: str, new_status: QuoteStatusEnum) -> Optional[Quote]:
        return await quote_service.change_quote_status(quote_id, new_status)

    @strawberry.mutation
    async def delete_quote(self, id: str) -> bool:
        return await quote_service.delete_quote(id)

schema = strawberry.Schema(query=Query, mutation=Mutation)
