"""
Order management router
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db import get_db
from app.models import Order, OrderItem, MenuItem, Table
from app.schemas import (
    OrderCreate, OrderUpdate, OrderResponse, OrderStatus,
    MessageResponse, OrderItemCreate, OrderItemResponse
)
from app.utils import OrderCalculator, generate_order_number, log_activity
from app.config import settings

router = APIRouter()


def calculate_order_totals(order_items: List[OrderItem], db: Session) -> dict:
    """Calculate order totals based on order items"""
    calculator = OrderCalculator(
        tax_rate=0.08,  # 8% tax rate - should come from settings or restaurant config
        service_charge=0.0
    )
    
    # Calculate item totals
    for item in order_items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if menu_item:
            item.unit_price = menu_item.price
            item.total_price = calculator.calculate_item_total(menu_item.price, item.quantity)
    
    # Calculate order subtotal
    subtotal = sum(item.total_price for item in order_items)
    
    return calculator.calculate_totals(subtotal)


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    table_id: Optional[int] = Query(None, description="Filter by table ID"),
    date_from: Optional[datetime] = Query(None, description="Filter orders from date"),
    date_to: Optional[datetime] = Query(None, description="Filter orders to date"),
    db: Session = Depends(get_db)
):
    """Get all orders with filtering options"""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status.value)
    
    if table_id:
        query = query.filter(Order.table_id == table_id)
    
    if date_from:
        query = query.filter(Order.created_at >= date_from)
    
    if date_to:
        query = query.filter(Order.created_at <= date_to)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """Create a new order"""
    # Verify table exists and is available
    table = db.query(Table).filter(Table.id == order.table_id).first()
    if not table:
        raise HTTPException(status_code=400, detail="Table not found")
    
    if not table.is_available:
        raise HTTPException(status_code=400, detail="Table is not available")
    
    # Create order
    order_data = order.model_dump(exclude={"items"})
    db_order = Order(**order_data)
    db.add(db_order)
    db.flush()  # Flush to get order ID
    
    # Create order items
    order_items = []
    for item_data in order.items:
        # Verify menu item exists and is available
        menu_item = db.query(MenuItem).filter(MenuItem.id == item_data.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=400, detail=f"Menu item {item_data.menu_item_id} not found")
        
        if not menu_item.is_available:
            raise HTTPException(status_code=400, detail=f"Menu item '{menu_item.name}' is not available")
        
        # Create order item
        order_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=item_data.menu_item_id,
            quantity=item_data.quantity,
            unit_price=menu_item.price,
            total_price=menu_item.price * item_data.quantity,
            special_instructions=item_data.special_instructions
        )
        order_items.append(order_item)
        db.add(order_item)
    
    # Calculate totals
    totals = calculate_order_totals(order_items, db)
    db_order.subtotal = totals["subtotal"]
    db_order.tax = totals["tax"]
    db_order.total = totals["total"]
    
    # Mark table as unavailable
    table.is_available = False
    
    db.commit()
    db.refresh(db_order)
    
    log_activity("order_created", details={"order_id": db_order.id, "table_id": order.table_id})
    
    return db_order


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Update an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify table exists if being updated
    if order_update.table_id:
        table = db.query(Table).filter(Table.id == order_update.table_id).first()
        if not table:
            raise HTTPException(status_code=400, detail="Table not found")
    
    # Update order
    update_data = order_update.model_dump(exclude_unset=True)
    
    # Handle status changes
    if "status" in update_data:
        old_status = order.status
        new_status = update_data["status"]
        
        # Handle table availability when order is completed/cancelled
        if new_status in ["paid", "cancelled"] and old_status not in ["paid", "cancelled"]:
            if order.table:
                order.table.is_available = True
        
        # Set completion time
        if new_status == "paid":
            update_data["completed_at"] = datetime.utcnow()
    
    # Update fields
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    
    log_activity("order_updated", details={"order_id": order_id, "updates": list(update_data.keys())})
    
    return order


@router.delete("/{order_id}", response_model=MessageResponse)
async def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """Cancel an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status in ["paid", "cancelled"]:
        raise HTTPException(status_code=400, detail="Cannot cancel a completed or already cancelled order")
    
    # Update order status
    order.status = "cancelled"
    
    # Make table available
    if order.table:
        order.table.is_available = True
    
    db.commit()
    
    log_activity("order_cancelled", details={"order_id": order_id})
    
    return MessageResponse(message="Order cancelled successfully")


@router.post("/{order_id}/items", response_model=OrderItemResponse, status_code=201)
async def add_item_to_order(
    order_id: int,
    item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    """Add an item to an existing order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status in ["paid", "cancelled"]:
        raise HTTPException(status_code=400, detail="Cannot modify a completed or cancelled order")
    
    # Verify menu item exists and is available
    menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=400, detail="Menu item not found")
    
    if not menu_item.is_available:
        raise HTTPException(status_code=400, detail="Menu item is not available")
    
    # Create order item
    order_item = OrderItem(
        order_id=order_id,
        menu_item_id=item.menu_item_id,
        quantity=item.quantity,
        unit_price=menu_item.price,
        total_price=menu_item.price * item.quantity,
        special_instructions=item.special_instructions
    )
    
    db.add(order_item)
    
    # Recalculate order totals
    all_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    all_items.append(order_item)  # Include the new item
    
    totals = calculate_order_totals(all_items, db)
    order.subtotal = totals["subtotal"]
    order.tax = totals["tax"]
    order.total = totals["total"]
    
    db.commit()
    db.refresh(order_item)
    
    log_activity("order_item_added", details={"order_id": order_id, "menu_item_id": item.menu_item_id})
    
    return order_item


@router.delete("/{order_id}/items/{item_id}", response_model=MessageResponse)
async def remove_item_from_order(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Remove an item from an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status in ["paid", "cancelled"]:
        raise HTTPException(status_code=400, detail="Cannot modify a completed or cancelled order")
    
    order_item = db.query(OrderItem).filter(
        OrderItem.id == item_id,
        OrderItem.order_id == order_id
    ).first()
    
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    
    db.delete(order_item)
    
    # Recalculate order totals
    remaining_items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.id != item_id
    ).all()
    
    if remaining_items:
        totals = calculate_order_totals(remaining_items, db)
        order.subtotal = totals["subtotal"]
        order.tax = totals["tax"]
        order.total = totals["total"]
    else:
        # If no items left, set totals to zero
        order.subtotal = 0
        order.tax = 0
        order.total = 0
    
    db.commit()
    
    log_activity("order_item_removed", details={"order_id": order_id, "item_id": item_id})
    
    return MessageResponse(message="Item removed from order")


@router.get("/table/{table_id}/active", response_model=Optional[OrderResponse])
async def get_active_order_by_table(table_id: int, db: Session = Depends(get_db)):
    """Get active order for a specific table"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    active_order = db.query(Order).filter(
        Order.table_id == table_id,
        Order.status.notin_(["paid", "cancelled"])
    ).first()
    
    return active_order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    new_status: OrderStatus = Query(..., description="New order status"),
    db: Session = Depends(get_db)
):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    old_status = order.status
    
    # Validate status transition
    valid_transitions = {
        "pending": ["confirmed", "cancelled"],
        "confirmed": ["preparing", "cancelled"],
        "preparing": ["ready", "cancelled"],
        "ready": ["served"],
        "served": ["paid"],
        "paid": [],  # Final state
        "cancelled": []  # Final state
    }
    
    if new_status.value not in valid_transitions.get(old_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {old_status} to {new_status.value}"
        )
    
    order.status = new_status.value
    
    # Handle side effects
    if new_status.value in ["paid", "cancelled"] and old_status not in ["paid", "cancelled"]:
        # Free up the table
        if order.table:
            order.table.is_available = True
        
        # Set completion time if paid
        if new_status.value == "paid":
            order.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    log_activity("order_status_changed", details={
        "order_id": order_id,
        "old_status": old_status,
        "new_status": new_status.value
    })
    
    return order