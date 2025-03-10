from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.reponse import Response

from core.database import get_db1
from apps.user.schemas.user import UserView, UserCreate,UserUpdate,UserAuth,UserChangePassword,UserActive
from apps.user.services.user import get_users, create_user, get_user, delete_user, filter_users, update_user, login_user, user_change_password,user_activate,user_refresh_token, UUID, User
import json

router = APIRouter()

# Get all users
@router.get("/users", response_model=list[UserView])
async def get_all_users(db: AsyncSession = Depends(get_db1)):
    users = await get_users(db)
    return users

# Get a single user by ID
@router.get("/users/{user_id}")
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db1)):
    user = await get_user(db, user_id)
    return user

# Create a new user
@router.post("/users", response_model=UserCreate, status_code=201)
async def create_new_user(user_create: UserCreate, db: AsyncSession = Depends(get_db1)):
    
    try:
        result = await db.execute(select(User).filter(User.email == user_create.email))
        if len(result.scalars().all())>0:
            return Response(message=f"User with email-'{user_create.email}' Already Exists",success=False,code=400)

        created_user = await create_user(db, user_create)
        if created_user is None:
            return Response(message="User not Created",success=False,code=404)
        return Response(data=created_user.to_dict(),code=201)

    except Exception as error:
        return Response(message=str(error), success=False,code=500)

# Update an existing user
@router.put("/users/{user_id}", response_model=UserView)
async def update_user_by_id(user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db1)):
    try:
        updated_user = await update_user(db, user_update, user_id)
        if updated_user is None:
            return Response(message="User not found",success=False,code=404)
        user = updated_user.to_dict()
        user.pop("access_token", None)  # Remove access_token if it exists
        user.pop("refresh_token", None)  # Remove refresh_token if it exists
        return Response(data=user,message='User Updated Successfully',code=200)

    except Exception as error:
        return Response(message=str(error), success=False,code=500)

# Delete a user
@router.delete("/users/{user_id}", status_code=204)
async def delete_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db1)):
    try:
        await delete_user(db, user_id)
        return Response(message="User successfully deleted",code=200)
    except Exception as error:
        return Response(message=str(error.message or error), success=False, code=error.code or 500)

# Filter users by dynamic criteria
@router.post("/users/filter")
async def filter_users_by_criteria(filters: dict,  db: AsyncSession = Depends(get_db1)):
    try:
        users = await filter_users(db, filters)
        
        return Response(data=users,code=200)
    except Exception as error:
        return Response(message=str(error),success=False,code=500)
    
@router.post("/users/login")
async def login(user_auth: UserAuth, db: AsyncSession = Depends(get_db1)):
    try:
        if user_auth.email is None or user_auth.email == '':
            return Response(message='email is needed',success=False,code=400)

        if user_auth.password is None or user_auth.password == '':
            return Response(message='password is needed',success=False,code=400)

        result = await db.execute(select(User).filter(User.email == user_auth.email).options(selectinload(User.addresses)))
        user = result.scalars().first()
        if user is None:
            return Response(message="User not found",success=False,code=404)

        correctpassword = user.verify_password(user_auth.password)
        
        if not correctpassword:
            return Response(message='password is incorrect',success=False,code=400)

        loggedin_user = await login_user(db,user)
        
        return Response(data=loggedin_user, message='User loggedin successfully',code=200)

    except Exception as error:
        return Response(message=str(error),success=False,code=500)

@router.post("/users/delete-account")
async def delete_user_by_self(user_auth: UserAuth, db: AsyncSession = Depends(get_db1)):
    try:
        if user_auth.email is None or user_auth.email == '':
            return Response(message='email is needed',success=False,code=400)

        if user_auth.password is None or user_auth.password == '':
            return Response(message='password is needed',success=False,code=400)

        result = await db.execute(select(User).filter(User.email == user_auth.email).options(selectinload(User.addresses)))
        user = result.scalars().first()
        if user is None:
            return Response(message="User not found",success=False,code=404)

        correctpassword = user.verify_password(user_auth.password)
        if not correctpassword:
            return Response(message='password is incorrect',success=False,code=400)

        deleted = await delete_user(db, user.id)
        return Response(message="User successfully deleted",code=200)

    except Exception as error:
        return Response(message=str(error),success=False,code=500)

@router.post("/users/change-password")
async def change_user_password(user_password: UserChangePassword, db: AsyncSession = Depends(get_db1)):
    try:
        if user_password.email is None or user_password.email == '':
            return Response(message='email is needed',success=False,code=400)

        if user_password.oldpassword is None or user_password.oldpassword == '':
            return Response(message='Old password is needed',success=False,code=400)

        if user_password.newpassword is None or user_password.newpassword == '':
            return Response(message='New password is needed',success=False,code=400)

        result = await db.execute(select(User).filter(User.email == user_password.email).options(selectinload(User.addresses)))
        user = result.scalars().first()
        if user is None:
            return Response(message="User not found",success=False,code=404)

        correctoldpassword = user.verify_password(user_password.oldpassword)
        if not correctoldpassword:
            return Response(message='Old password is incorrect',success=False,code=400)

        user_changed = await user_change_password(db, user, user_password.newpassword)
        return Response(message="User Password Changed Successfully",data=user_changed,code=200)

    except Exception as error:
        return Response(message=str(error),success=False,code=500)

@router.post("/users/verify-email")
async def verify_user_email(user_active: UserActive, db: AsyncSession = Depends(get_db1)):
    try:
        if user_active.email is None or user_active.email == '':
            return Response(message='email is needed',success=False,code=400)

        result = await db.execute(select(User).filter(User.email == user_active.email).options(selectinload(User.addresses)))
        user = result.scalars().first()
        if user is None:
            return Response(message="User not found",success=False,code=404)

        user_activated = await user_activate(db, user, True)
        return Response(message="User Activated Successfully",data=user_activated,code=200)

    except Exception as error:
        return Response(message=str(error),success=False,code=500)

@router.post("/users/deactivate")
async def deactivate_user(user_active: UserActive, db: AsyncSession = Depends(get_db1)):
    try:
        if user_active.email is None or user_active.email == '':
            return Response(message='email is needed',success=False,code=400)

        result = await db.execute(select(User).filter(User.email == user_active.email).options(selectinload(User.addresses)))
        user = result.scalars().first()
        if user is None:
            return Response(message="User not found",success=False,code=404)

        user_deactivated = await user_activate(db, user, False)
        return Response(message="User Deactivated Successfully",data=user_deactivated,code=200)

    except Exception as error:
        return Response(message=str(error),success=False,code=500)
     
@router.post("/users/refresh_access_token")
async def refresh_user_access_token(user_auth: UserAuth, db: AsyncSession = Depends(get_db1)):
    try:
        if user_auth.email is None or user_auth.email == '':
            return Response(message='email is needed',success=False,code=400)

        if user_auth.password is None or user_auth.password == '':
            return Response(message='password is needed',success=False,code=400)

        result = await db.execute(select(User).filter(User.email == user_auth.email).options(selectinload(User.addresses)))
        user = result.scalars().first()
        if user is None:
            return Response(message="User not found",success=False,code=404)

        correctpassword = user.verify_password(user_auth.password)
        
        if not correctpassword:
            return Response(message='password is incorrect',success=False,code=400)
        
        new_user_token = await user_refresh_token(db, user)
        if not new_user_token:
            return Response(message='You need to login',success=False,code=401)
        return Response(message="New Access Token Gotten Successfully",data=new_user_token,code=200)

    except Exception as error:
        return Response(message=str(error),success=False,code=500)