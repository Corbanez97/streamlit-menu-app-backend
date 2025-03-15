from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class OrderItemCreate(BaseModel):
    """Schema for adding an item to an order."""
    order_id: UUID # References orders(id)
    menu_item_id: UUID  # References menu_items(id)
    quantity: int  # Must be greater than 0
    price: float  # Price at the time of order

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    """Schema for creating a new order."""
    user_id: UUID | None = None  # Nullable foreign key to users(id)
    items: list[OrderItemCreate]  # List of items in the order
    status: str = "pending"  # Default status
    created_at: datetime | None = None  # Auto-filled by the database

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    """Schema for updating an existing order."""
    items: list[OrderItemCreate] | None = None
    status: str | None = None

    class Config:
        from_attributes = True
