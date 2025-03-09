from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.reponse import Response
from core.database import get_db1
from apps.user.schemas.user import UserView, UserCreate,UserUpdate
from apps.user.services.user import get_users, create_user, get_user, delete_user, filter_users,update_user, UUID

router = APIRouter()

# Get all users
@router.get("/users", response_model=list[UserView])
async def get_all_users(db: AsyncSession = Depends(get_db1)):
    try:
        users = await get_users(db)
        return Response(data=users,code=200)
    except Exception as error:
        return Response(message=str(error),success=False,code=500)

# Get a single user by ID
@router.get("/users/{user_id}", response_model=UserView)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db1)):
    try:
        user = await get_user(db, user_id)
        sd
        if user is None:
            return Response(message="User not found",success=False,code=404)
        return Response(data=user,code=200)
    except Exception as error:
        return Response(message=str(error), success=False,code=500)

# Create a new user
@router.post("/users", response_model=UserView, status_code=201)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db1)):
    try:
        created_user = await create_user(db, user)
        if created_user is None:
            return Response(message="User not Created",success=False,code=404)
        return Response(data=created_user,code=201)

    except Exception as error:
        return Response(message=str(error), success=False,code=500)

# Update an existing user
@router.put("/users/{user_id}", response_model=UserView)
async def update_user_by_id(user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db1)):
    try:
        updated_user = await update_user(db, user_update, user_id)
        if updated_user is None:
            return Response(message="User not found",success=False,code=404)
        return Response(data=updated_user,code=200)

    except Exception as error:
        return Response(message=str(error), success=False,code=500)

# Delete a user
@router.delete("/users/{user_id}", status_code=204)
async def delete_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db1)):
    try:
        await delete_user(db, user_id)
        return Response(message="User successfully deleted",code=200)
    except Exception as error:
        return Response(message=str(error), success=False,code=500)

# Filter users by dynamic criteria
@router.get("/users/filter", response_model=list[UserView])
async def filter_users_by_criteria(filters: dict, db: AsyncSession = Depends(get_db1)):
    try:
        users = await filter_users(db, **filters)
        return Response(data=users,code=200)
    except Exception as error:
        return Response(message=str(error),success=False,code=500)
    