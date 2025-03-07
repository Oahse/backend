from fastapi import APIRouter, HTTPException, status
from typing import List
from src.services.user_service import get_user, create_user, update_user, delete_user, get_all_users
from src.schemas.user_schema import UserCreate, User, UserUpdate

router = APIRouter()

# Get a single user by ID
@router.get("/users/{user_id}", response_model=User, responses={404: {"description": "User not found"}})
async def get_user_by_id(user_id: int):
    """
    Retrieve a user by their unique user_id.
    If no user is found, returns a 404 error with a user-friendly message.
    """
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new user
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate):
    """
    Create a new user in the system.
    Takes user details and creates a new user record in the database.
    Returns the created user object.
    """
    return await create_user(user)

# Update a user's information
@router.put("/users/{user_id}", response_model=User, responses={404: {"description": "User not found"}})
async def update_user_by_id(user_id: int, user: UserUpdate):
    """
    Update an existing user's information based on their user_id.
    Returns the updated user object or a 404 if the user does not exist.
    """
    updated_user = await update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Delete a user by ID
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "User not found"}})
async def delete_user_by_id(user_id: int):
    """
    Delete a user by their user_id.
    Returns a 204 status code (No Content) on success or a 404 if the user is not found.
    """
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User successfully deleted"}

# Get all users
@router.get("/users", response_model=List[User], response_model_exclude_unset=True)
async def get_all_users_list():
    """
    Retrieve a list of all users in the system.
    Returns a list of user objects.
    """
    return await get_all_users()

