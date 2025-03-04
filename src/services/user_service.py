from src.repositories.user_repository import find_user_by_id, insert_new_user
from src.schemas.user_schema import UserCreate
from src.models.user_model import User

async def get_user(user_id: int) -> User:
    return await find_user_by_id(user_id)

async def create_user(user_create: UserCreate) -> User:
    return await insert_new_user(user_create)
