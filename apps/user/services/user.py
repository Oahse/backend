from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from apps.user.models.user import User, UUID
from apps.user.schemas.user import UserCreate, UserUpdate
from uuid import UUID
from fastapi import HTTPException

# Get all users (asynchronous)
async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Get a single user by ID (asynchronous)
async def get_user(db: AsyncSession, user_id: UUID):
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        
    except Exception as e:
        print(e,'====')
        return e
    return result.scalars().first()

# Create a new user (asynchronous)
async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        password=user.password,
        email=user.email,
        role=user.role,
        phone_number=user.phone_number,
        phone_number_pre=user.phone_number_pre,
        tags=user.tags,
        notes=user.notes
    )
    db.add(db_user)
    await db.commit()  # Use await here for async commit
    await db.refresh(db_user)  # Use await to refresh the instance
    return db_user

# Update an existing user (asynchronous)
async def update_user(db: AsyncSession, user_update: UserUpdate, user_id: UUID):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.firstname:
        db_user.firstname = user_update.firstname
    if user_update.lastname:
        db_user.lastname = user_update.lastname
    if user_update.password:
        db_user.password = user_update.password
    if user_update.email:
        db_user.email = user_update.email
    if user_update.role:
        db_user.role = user_update.role
    if user_update.phone_number:
        db_user.phone_number = user_update.phone_number
    if user_update.phone_number_pre:
        db_user.phone_number_pre = user_update.phone_number_pre
    if user_update.tags:
        db_user.tags = user_update.tags
    if user_update.notes:
        db_user.notes = user_update.notes

    await db.commit()
    await db.refresh(db_user)
    return db_user

# Delete a user (asynchronous)
async def delete_user(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(db_user)
    await db.commit()

# Filter users dynamically (asynchronous)
async def filter_users(db: AsyncSession, **filters):
    query = select(User)
    
    for field, value in filters.items():
        if hasattr(User, field):
            query = query.filter(getattr(User, field) == value)
    
    result = await db.execute(query)
    return result.scalars().all()
