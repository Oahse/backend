from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy import Enum, Integer, String, DateTime, ForeignKey, Boolean, Float
from core.database import Base, CHAR_LENGTH
from core.utils.encryption import PasswordManager
from uuid import uuid4  # to generate unique UUIDs
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional
from apps.products.models.currency import Currency
from apps.products.models.category import UUIDType,mappeditem,default,Category,Clicks

# Enum for product status (Active, Inactive, Pending Approval, etc.)
class ProductStatus(PyEnum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    PENDING = 'Pending Approval'
    OUT_OF_STOCK = 'Out of Stock'
    DISCONTINUED = 'Discontinued'

# Enum for product condition (New, Used, Refurbished, etc.)
class ProductCondition(PyEnum):
    NEW = 'New'
    USED = 'Used'
    REFURBISHED = 'Refurbished'  


# Product Model
class Products(Base):
    __tablename__ = "products"
    
    id: Mapped[mappeditem] = mapped_column(UUIDType, primary_key=True, default=default)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    currency: Mapped[str] = mapped_column(ForeignKey("currencies.symbol"), nullable=False)  # ForeignKey referencing user (UUID)
    
    description: Mapped[str] = mapped_column(String(1000), nullable=False)  # Product description
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # Stock Keeping Unit
    
    # Price, Discount, and Final Price
    price: Mapped[Float] = mapped_column(Float, nullable=False)  # Regular price
    discount: Mapped[Optional[int]] = mapped_column(int, nullable=True)  # Discounted in %
    
    # Stock and availability
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Quantity available in stock
    stock_status: Mapped[str] = mapped_column(Enum(ProductStatus), default=ProductStatus.ACTIVE)  # Product availability status
    
    # Product Condition (e.g., New, Used, Refurbished)
    condition: Mapped[ProductCondition] = mapped_column(Enum(ProductCondition), default=ProductCondition.NEW)
    
    # Category and Brand
    category: Mapped[str] = mapped_column(ForeignKey("categories.name"), nullable=False)  # ForeignKey referencing user (UUID)
    subcategory: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Subcategory (e.g., Smartphones, Laptops)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)  # Brand of the product
    
    # Shipping Information
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Product weight in kg or lbs
    dimensions: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Dimensions for shipping (length, width, height)
    shipping_method: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Shipping methods supported
    free_shipping: Mapped[bool] = mapped_column(Boolean, default=False)  # Flag indicating if the product has free shipping
    
    # Product Media (Images and Video URLs)
    image_urls: Mapped[List[str]] = mapped_column(JSON, nullable=True)  # List of image URLs (JSON type to store multiple URLs)
    video_urls: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # List of video URLs for product demonstration
    
    # Reviews and Ratings
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Average rating (calculated from user reviews)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)  # Total number of reviews
    
    # Vendor/Supplier Information
    vendor_id: Mapped[UUID] = mapped_column(ForeignKey("vendors.id"), nullable=False)  # Foreign Key to the Vendor table
    vendor_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Vendor cost price for the product
    supplier_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Supplier's internal reference
    
    # Dates
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # When the product was created
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last updated timestamp
    
    # Product Status (Active, Inactive, etc.)
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), default=ProductStatus.ACTIVE)  # Product active status
    
    # Optional relationships (can be used for foreign key referencing)
    vendor: Mapped["Vendor"] = relationship("Vendor", back_populates="products")

    # Relationship back to Clicks
    clicks: Mapped[List[Clicks]] = relationship("Clicks", back_populates="product", cascade="all, delete-orphan")

    categories: Mapped[List[Category]] = relationship("Category", back_populates="product", cascade="all, delete-orphan")
    
    # Method to calculate the final price (taking into account discounts)
    @property
    def final_price(self):
        if self.discount:
            return self.price - (self.price*(self.discount/100))

        return self.price
    
    # Method to return a detailed dictionary representation of the product
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "currency":self.currency,
            "description": self.description,
            "sku": self.sku,
            "price": self.price,
            "discount_price": self.discount_price,
            "final_price": self.final_price,
            "stock_quantity": self.stock_quantity,
            "stock_status": self.stock_status.value,
            "condition": self.condition.value,
            "category": self.category.value,
            "subcategory": self.subcategory,
            "brand": self.brand,
            "weight": self.weight,
            "dimensions": self.dimensions,
            "shipping_method": self.shipping_method,
            "free_shipping": self.free_shipping,
            "image_urls": self.image_urls,
            "video_urls": self.video_urls,
            "rating": self.rating,
            "total_reviews": self.total_reviews,
            "vendor_id": str(self.vendor_id),
            "vendor_price": self.vendor_price,
            "supplier_reference": self.supplier_reference,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value
        }

    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.name!r}, brand={self.brand!r}, price={self.price!r})"
    

