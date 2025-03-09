from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum, Integer, String, DateTime, UUID, ForeignKey
from core.database import Base, CHAR_LENGTH
from uuid import uuid4  # to generate unique UUIDs
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional
from uuid import UUID
import sys

# Database type detection
if 'postgresql' in sys.argv:
    # Use native UUID for PostgreSQL
    UUIDType = UUID(as_uuid=True)
    mappeditem = UUID
    default = uuid4
else:
    # Use string representation for other databases
    UUIDType = String(36)
    mappeditem = str
    default = lambda: str(uuid4())

# Enum for Address types: Billing or Shipping
class AddressType(PyEnum):
    Billing = "Billing"
    Shipping = "Shipping"

class Address(Base):
    __tablename__ = "address"

    # Define the fields
    # Use UUID type with default to auto-generate UUID
    id: Mapped[mappeditem] = mapped_column(UUIDType, primary_key=True, default=default)  # UUID with auto-generation
    
    email_address: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Optional email field
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)  # ForeignKey referencing user (UUID)
    user: Mapped["User"] = relationship("User", back_populates="addresses")  # Relationship with User model
    
    street: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Optional street
    city: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Optional city
    state: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Optional state
    country: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Optional country
    post_code: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Optional postal code
    kind: Mapped[AddressType] = mapped_column(Enum(AddressType), nullable=False)  # Address type (either Billing or Shipping)

    # Optional timestamp for tracking address creation/updates
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Optional timestamp
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Auto update timestamp

    def __repr__(self):
        return f"Address(id={self.id!r}, kind={self.kind!r}, email_address={self.email_address!r})"

    


# Enum for user roles (make sure it's a valid Enum class)
class UserRole(PyEnum):
    Buyer = "Buyer"
    Seller = "Seller"
    Admin = "Admin"



class User(Base):
    __tablename__ = "user"
    
    # Use UUID type with default to auto-generate UUID
    id: Mapped[mappeditem] = mapped_column(UUIDType, primary_key=True, default=default)  # UUID with auto-generation
    
    # User details
    firstname: Mapped[str] = mapped_column(String(CHAR_LENGTH))  # First name as string
    lastname: Mapped[str] = mapped_column(String(CHAR_LENGTH))  # Last name as string
    password: Mapped[str] = mapped_column(String(CHAR_LENGTH))  # Password as string
    email: Mapped[str] = mapped_column(String(CHAR_LENGTH), unique=True, index=True)  # Email as unique string
    
    # Role as Enum with a non-nullable constraint
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)  # User role as Enum
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Created timestamp (UTC)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Updated timestamp (auto updates)
    
    # Additional fields
    totalorders: Mapped[int] = mapped_column(Integer, default=0)  # Total orders as integer
    phone_number: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Phone number as string (nullable)
    phone_number_pre: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Phone number prefix (nullable)
    tags: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Tags as string (nullable)
    notes: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=True)  # Notes as string (nullable)
    
    # Relationship with Address model
    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, role={self.role!r})"
    
    
