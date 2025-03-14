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
    # Use native UUID for PostgreSQL to handle UUIDs properly in the database
    UUIDType = UUID(as_uuid=True)
    mappeditem = UUID
    default = uuid4  # Use UUID4 for generating unique UUIDs by default
else:
    # Use string representation for other databases like SQLite or MySQL
    UUIDType = str
    mappeditem = str
    default = lambda: str(uuid4())  # Use string representation for UUIDs in other databases

# Enum for user roles (used in the schema)
class UserRole(str, Enum):
    # Defining possible user roles as an Enum for better type safety and validation
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
    # Base schema containing common fields for a User, used in both creation and updates
    firstname: str  # User's first name
    lastname: str   # User's last name
    email: str      # User's email address
    totalorders: Optional[int] = None  # Optional field to track total orders placed by the user
    phone_number: Optional[str] = None  # Optional field for user's phone number
    phone_number_pre: Optional[str] = None  # Optional field for phone number prefix (e.g., country code)
    tags: Optional[str] = None  # Optional tags associated with the user (e.g., "VIP", "Premium")
    notes: Optional[str] = None  # Optional field for additional notes on the user
    access_token: Optional[str] = None  # Optional field for storing the access token (JWT)
    refresh_token: Optional[str] = None  # Optional field for storing the refresh token (JWT)

    class Config:
        from_attributes = True  # Allows interaction with SQLAlchemy models to auto-map fields

# Pydantic schema for creating a User
class UserCreate(UserBase):
    # Schema used when creating a new user, extending the base schema to include role and password
    role: UserRole  # Role of the user (Buyer, Seller, etc.)
    password: str  # User's password for authentication

    pass

# Pydantic schema for updating an existing User
class UserUpdate(UserBase):
    # Schema used when updating an existing user, role is also included to allow role changes
    role: UserRole  # Role of the user (Buyer, Seller, etc.)
    pass

# Pydantic schema for User View with related addresses
class UserView(UserBase):
    # View schema for displaying user data, including related address information
    id: UUIDType  # User's unique ID (UUID or string depending on the database)
    role: UserRole  # Role of the user (Buyer, Seller, etc.)
    active: bool  # Status to indicate if the user is active
    addresses: List["AddressView"] = []  # List of associated address instances (from AddressView schema)

class UserActive(BaseModel):
    # Schema used for operations involving active users (e.g., login)
    email: str  # User's email address
    
class UserAuth(UserActive):
    # Schema for user authentication with email and password fields
    password: str  # User's password for authentication

class UserChangePassword(UserActive):
    # Schema for changing a user's password (requires old password and new password)
    oldpassword: str  # User's current password
    newpassword: str  # User's new password

# Role-specific User Create schemas for each user role

class GuestCreate(UserBase):
    role: UserRole = UserRole.Guest  # Default role is Guest
    password: str  # Password for the guest user

    class Config:
        from_attributes = True

class BuyerCreate(UserBase):
    role: UserRole = UserRole.Buyer  # Default role is Buyer
    password: str  # Password for the buyer user

    class Config:
        from_attributes = True

class SellerCreate(UserBase):
    role: UserRole = UserRole.Seller  # Default role is Seller
    password: str  # Password for the seller user

    class Config:
        from_attributes = True

class AdminCreate(UserBase):
    role: UserRole = UserRole.Admin  # Default role is Admin
    password: str  # Password for the admin user

    class Config:
        from_attributes = True

class GodAdminCreate(UserBase):
    role: UserRole = UserRole.GodAdmin  # Default role is GodAdmin
    password: str  # Password for the GodAdmin user

    class Config:
        from_attributes = True

class SuperAdminCreate(UserBase):
    role: UserRole = UserRole.SuperAdmin  # Default role is SuperAdmin
    password: str  # Password for the SuperAdmin user

    class Config:
        from_attributes = True

class ModeratorCreate(UserBase):
    role: UserRole = UserRole.Moderator  # Default role is Moderator
    password: str  # Password for the moderator user

    class Config:
        from_attributes = True

class SupportCreate(UserBase):
    role: UserRole = UserRole.Support  # Default role is Support
    password: str  # Password for the support user

    class Config:
        from_attributes = True

class ManagerCreate(UserBase):
    role: UserRole = UserRole.Manager  # Default role is Manager
    password: str  # Password for the manager user

    class Config:
        from_attributes = True


# Update forward references for Pydantic to handle circular references
UserView.update_forward_refs()
