from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from apps.user.models.user import User, UUID
from apps.user.schemas.user import UserCreate, UserUpdate, UserView, UserAuth,UserChangePassword
from uuid import UUID
from fastapi import HTTPException
from core.utils.auth.jwt_auth import JWTManager
from core.utils.reponse import Response
from core.utils.encryption import PasswordManager
import sys, json

# Define a custom exception for user not found
class UserNotFoundException(Exception):
    def __init__(self, message="User not found", code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


# Database type detection
if 'postgresql' in sys.argv:
    # Use native UUID for PostgreSQL
    UUIDType = UUID(as_uuid=True)
    mappeditem = UUID
    default = uuid4
else:
    # Use string representation for other databases
    UUIDType = str
    mappeditem = str
    default = lambda: str(uuid4())
    
# Get all users (asynchronous)
async def get_users(db: AsyncSession):
    try:
        result = await db.execute(select(User).options(selectinload(User.addresses)))
        # Get all users as a list of dictionaries
        users = []
        
        # Remove sensitive keys from each user's dictionary
        for user in result.scalars().all():
            user_ = user.to_dict()
            user_.pop("access_token", None)  # Remove access_token if it exists
            user_.pop("refresh_token", None)  # Remove refresh_token if it exists

            users.append(user_)
        return Response(data=users,code=200)
    except Exception as error:
        return Response(message=str(error),success=False,code=500)

# Get a single user by ID (asynchronous)
async def get_user(db: AsyncSession, user_id: UUID):
    uid = str(user_id) if UUIDType is str else user_id
    
    try:
        result = await db.execute(select(User).filter(User.id == uid).options(selectinload(User.addresses)))
        user = result.scalars().first()
        if not user:
            return Response(message="User not found",success=False,code=404)
        return Response(data=user.to_dict(),code=200)
    except Exception as error:
        return Response(message=str(error), success=False, code=500)
    

# Create a new user (asynchronous)
async def create_user(db: AsyncSession, user: UserCreate):
    password_manager = PasswordManager()

    # Hash the password
    hashed_password = password_manager.hash_password(user.password)
    jwt_manager = JWTManager(secret_key=hashed_password)
    jsonuser = json.loads(user.json())

    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        password=hashed_password,
        email=user.email,
        role=user.role,
        phone_number=user.phone_number,
        phone_number_pre=user.phone_number_pre,
        active=False,
        tags=user.tags,
        notes=user.notes,
        access_token=jwt_manager.create_access_token(jsonuser),
        refresh_token=jwt_manager.create_refresh_token(jsonuser)
    )
    db.add(db_user)
    await db.commit()  # Use await here for async commit
    await db.refresh(db_user)  # Use await to refresh the instance
    return db_user

# Update an existing user (asynchronous)
async def update_user(db: AsyncSession, user_update: UserUpdate, user_id: UUID):
    uid = str(user_id) if UUIDType is str else user_id
    result = await db.execute(select(User).filter(User.id == uid).options(selectinload(User.addresses)))
    db_user = result.scalars().first()
    if not db_user:
        raise UserNotFoundException(message="User not found")

    if user_update.firstname:
        db_user.firstname = user_update.firstname
    if user_update.lastname:
        db_user.lastname = user_update.lastname
    
    if user_update.email:
        db_user.email = user_update.email
    if user_update.role:
        db_user.role = user_update.role
    if user_update.active:
        db_user.active = user_update.active
    if user_update.phone_number:
        db_user.phone_number = user_update.phone_number
    if user_update.phone_number_pre:
        db_user.phone_number_pre = user_update.phone_number_pre
    if user_update.tags:
        db_user.tags = user_update.tags
    if user_update.notes:
        db_user.notes = user_update.notes
    if user_update.access_token:
        db_user.access_token = user_update.access_token
    if user_update.refresh_token:
        db_user.refresh_token = user_update.refresh_token

    await db.commit()
    await db.refresh(db_user)
    return db_user

# Delete a user (asynchronous)
async def delete_user(db: AsyncSession, user_id: UUID):
    uid = str(user_id) if UUIDType is str else user_id
    result = await db.execute(select(User).filter(User.id == uid).options(selectinload(User.addresses)))
    db_user = result.scalars().first()
    if not db_user:
        raise UserNotFoundException(message="User not found", code=404)
    await db.delete(db_user)
    await db.commit()

# Filter users dynamically (asynchronous)
async def filter_users(db: AsyncSession, filters: dict):
    # Start with the base query
    query = select(User)
    
    # Apply filters dynamically
    for field, value in filters.items():
        if hasattr(User, field):  # Check if User model has the attribute (field)
            query = query.filter(getattr(User, field) == value).options(selectinload(User.addresses))

    # Execute the query after all filters are applied
    result = await db.execute(query)
    
    # Get all users as a list of dictionaries
    res=result.scalars().all()
    users = []
    print(res)
    # Remove sensitive keys from each user's dictionary
    for user in res:
        user_dict = user.to_dict()  # Assuming you have a method to convert to dict
        user_dict.pop("access_token", None)  # Remove sensitive information like access tokens
        user_dict.pop("refresh_token", None)
        
        users.append(user_dict)
    return users

async def login_user(db: AsyncSession, user_update: UserUpdate):
    jsonuser = user_update.to_dict()

    password_manager = PasswordManager()

    # Hash the password
    hashed_password = password_manager.hash_password(user_update.password)
    jwt_manager = JWTManager(secret_key=hashed_password)
    
    user_update.access_token = jwt_manager.create_access_token(jsonuser)
    user_update.refresh_token = jwt_manager.create_refresh_token(jsonuser)

    await db.commit()
    await db.refresh(user_update)

    return user_update.to_dict()

async def user_change_password(db: AsyncSession, user: UserUpdate,newpassword: str):
    password_manager = PasswordManager()

    # Hash the password
    user.password = password_manager.hash_password(newpassword)
    
    await db.commit()
    await db.refresh(user)
    user_ = user.to_dict()
    user_.pop("access_token", None)  # Remove access_token if it exists
    user_.pop("refresh_token", None)  # Remove refresh_token if it exists

    return user_

async def user_activate(db: AsyncSession, user: UserUpdate, active:bool = True):
    user.active = active
    
    await db.commit()
    await db.refresh(user)
    user_ = user.to_dict()
    user_.pop("access_token", None)  # Remove access_token if it exists
    user_.pop("refresh_token", None)  # Remove refresh_token if it exists

    return user_

async def user_refresh_token(db: AsyncSession, user: UserUpdate):

    # verify the refresh token
    # if invalid return invalid you need to login
    # if valid generate a new access token usng the refresh token
    u=user.to_dict()
    u.pop("access_token", None)  # Remove access_token if it exists
    u.pop("refresh_token", None)  # Remove refresh_token if it exists
    jwt_manager = JWTManager(secret_key=user.password)

    try:
        decoded_refresh_data = jwt_manager.verify_token(user.refresh_token)
        # print("Decoded Refresh Token Data:", decoded_refresh_data)
        await db.commit()
        await db.refresh(user)
        
        user.access_token = jwt_manager.create_access_token(u)

        return user.to_dict()
        
    except Exception as e:
        # auth is needed
        return False
    
    
