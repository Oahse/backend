from sqlalchemy import Integer, String, DateTime, UUID, ForeignKey
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4
from apps.user.schemas.address import AddressView
import sys

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

# Enum for user roles (used in the schema)
class UserRole(str, Enum):
    Guest = 'Guest'
    Buyer = "Buyer"
    Seller = "Seller"
    Admin = "Admin"
    GodAdmin = "GodAdmin"
    SuperAdmin = "SuperAdmin"
    Moderator = "Moderator"
    Support = "Support"
    Manager = "Manager"

# Pydantic schema for User View (includes relationships and additional fields)
class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    role: UserRole
    totalorders: Optional[int] = None
    phone_number: Optional[str] = None
    phone_number_pre: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    class Config:
        from_attributes = True # Allows interaction with SQLAlchemy models

# Pydantic schema for creating a User
class UserCreate(UserBase):
    password: str
    pass

# Pydantic schema for updating an existing User
class UserUpdate(UserBase):
    pass


# Pydantic schema for User View with related addresses
class UserView(UserBase):
    id: UUIDType  # Using UUID as the proper type for the user ID
    active: bool
    addresses: List["AddressView"] = []  # List of AddressView schema instances

class UserActive(BaseModel):
    email: str
    
class UserAuth(UserActive):
    password: str

class UserChangePassword(UserActive):
    oldpassword: str
    newpassword: str



# Token data that will be sent to the user
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Update forward references for Pydantic
UserView.update_forward_refs()