from typing import List
from app.schemas.user import User, UserInput

class UserService:
    def __init__(self):
        # Données en mémoire pour l'exemple
        self.users: List[User] = [
            User(id=1, name="Alice", email="alice@example.com", age=30),
            User(id=2, name="Bob", email="bob@example.com", age=25),
        ]
        self.next_id = 3

    def get_all_users(self) -> List[User]:
        return self.users

    def get_user_by_id(self, user_id: int) -> User | None:
        return next((user for user in self.users if user.id == user_id), None)

    def create_user(self, user_input: UserInput) -> User:
        new_user = User(
            id=self.next_id,
            name=user_input.name,
            email=user_input.email,
            age=user_input.age
        )
        self.users.append(new_user)
        self.next_id += 1
        return new_user

    def update_user(self, user_id: int, user_input: UserInput) -> User | None:
        user = self.get_user_by_id(user_id)
        if user:
            user.name = user_input.name
            user.email = user_input.email
            user.age = user_input.age
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False
