from fastapi import APIRouter
from typing import List
from src.services.user_service import get_user, create_user
from src.schemas.user_schema import UserCreate, User

router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    return await get_user(user_id)

@router.post("/users", response_model=User)
async def create_new_user(user: UserCreate):
    return await create_user(user)
