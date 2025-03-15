from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from uuid import UUID

from backend.database import get_db
from backend.models.orders import Order, OrderItem
from backend.models.menu import MenuItem
from backend.schemas.orders import OrderCreate, OrderUpdate, OrderItemCreate

router = APIRouter()

@router.get("/orders/")
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    """Retrieve all orders."""
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders

@router.get("/orders/{order_id}")
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a specific order by ID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/{order_id}/total")
async def get_order_total(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve the total price of a given order."""
    result = await db.execute(
        select(func.sum(OrderItem.price * OrderItem.quantity))
        .where(OrderItem.order_id == order_id)
    )
    
    total = result.scalar()
    
    if total is None:
        raise HTTPException(status_code=404, detail="Order not found or has no items")
    
    return {"order_id": order_id, "total": float(total)}

@router.get("/orders/{order_id}/items")
async def get_order_items(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve all items belonging to a specific order."""
    result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order_id)
    )
    
    items = result.scalars().all()
    
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this order")

    return items

@router.post("/orders/")
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    """Create a new order with items."""
    try:
        new_order = Order(status="pending")
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        return {"message": "Order created successfully!", "order": new_order}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@router.post("/orders/{order_id}/items")
async def add_order_item(order_id: UUID, item_data: OrderItemCreate, db: AsyncSession = Depends(get_db)):
    """Add an item to an existing order."""
    # Validate if order exists
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Validate if menu item exists
    menu_item = await db.get(MenuItem, item_data.menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    # Create the order item
    new_order_item = OrderItem(
        order_id=order_id,
        menu_item_id=item_data.menu_item_id,
        quantity=item_data.quantity,
        price=menu_item.price  # Store price at time of order
    )

    db.add(new_order_item)
    await db.commit()
    await db.refresh(new_order_item)

    return {"message": "Order item added successfully!", "order_item": new_order_item}

@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: UUID, 
    order_update: OrderUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Update the status of an order."""
    order = await db.get(Order, order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order_update.status:
        order.status = order_update.status

    await db.commit()
    await db.refresh(order)

    return {"message": "Order status updated successfully", "order": order}

@router.delete("/orders/{order_id}")
async def delete_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an order and its items."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await db.delete(order)
    await db.commit()

    return {"message": "Order deleted successfully"}

@router.delete("/orders/{order_id}/items/{item_id}")
async def delete_order_item(order_id: UUID, item_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an item from an order."""
    order_item = await db.get(OrderItem, item_id)
    if not order_item or order_item.order_id != order_id:
        raise HTTPException(status_code=404, detail="Order item not found")

    await db.delete(order_item)
    await db.commit()

    return {"message": "Order item deleted successfully"}
