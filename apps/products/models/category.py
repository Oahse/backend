from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy import Enum, Integer, String, DateTime, ForeignKey, Boolean
from core.database import Base, CHAR_LENGTH
from core.utils.encryption import PasswordManager
from uuid import uuid4  # to generate unique UUIDs
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional
from uuid import UUID
import sys
from apps.user.models.activities import Clicks


# Database type detection for UUID support
if 'postgresql' in sys.argv:
    UUIDType = UUID(as_uuid=True)
    mappeditem = UUID
    default = uuid4
else:
    UUIDType = String(36)
    mappeditem = str
    default = lambda: str(uuid4())

class Categories(Base):
    __tablename__ = "categories"
    
    id: Mapped[mappeditem] = mapped_column(UUIDType, primary_key=True, default=default)
    name: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=False)
    
    # Relationship back to Clicks
    clicks: Mapped[List[Clicks]] = relationship("Clicks", back_populates="category", cascade="all, delete-orphan")

