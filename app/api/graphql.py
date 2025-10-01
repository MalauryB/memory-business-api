import strawberry
from typing import List
from app.schemas.user import User, UserInput
from app.services.user_service import UserService

user_service = UserService()

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL!"

    @strawberry.field
    def users(self) -> List[User]:
        return user_service.get_all_users()

    @strawberry.field
    def user(self, id: int) -> User | None:
        return user_service.get_user_by_id(id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, user_input: UserInput) -> User:
        return user_service.create_user(user_input)

    @strawberry.mutation
    def update_user(self, id: int, user_input: UserInput) -> User | None:
        return user_service.update_user(id, user_input)

    @strawberry.mutation
    def delete_user(self, id: int) -> bool:
        return user_service.delete_user(id)

schema = strawberry.Schema(query=Query, mutation=Mutation)
