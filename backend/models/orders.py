import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, DECIMAL, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

from .menu import MenuItem

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    # Relationship to OrderItem
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True, nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)  # Store price at the time of order
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    # Relationship to Order
    order = relationship("Order", back_populates="items")
    # Relationship to MenuItem
    menu_item = relationship("MenuItem", back_populates="orders_items")
