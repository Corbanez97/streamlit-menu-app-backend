from pydantic import BaseModel
from uuid import UUID


class MenuItemCreate(BaseModel):
    """Schema for creating a new menu item."""
    id: UUID | None = None  # Optional UUID, auto-generated
    restaurant_id: UUID | None = None
    name: str
    description: str | None = None
    price: float
    image_url: str | None = None
    category: str  # "food", "drink", etc.

    class Config:
        from_attributes = True  # Allows SQLAlchemy-to-Pydantic conversion


class MenuItemUpdate(BaseModel):
    """Schema for updating an existing menu item."""
    id: UUID | None = None
    restaurant_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    image_url: str | None = None
    category: str | None = None
    available: bool | None = None

    class Config:
        from_attributes = True
