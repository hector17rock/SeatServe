"""
Menu management router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.models import Category, MenuItem
from app.schemas import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    MenuItemCreate, MenuItemUpdate, MenuItemResponse,
    MessageResponse, PaginatedResponse
)
from app.utils import get_pagination_params, calculate_pagination_info

router = APIRouter()


# Category endpoints
@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = Query(0, ge=0, description="Number of categories to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of categories to return"),
    active_only: bool = Query(True, description="Return only active categories"),
    db: Session = Depends(get_db)
):
    """Get all menu categories"""
    query = db.query(Category)
    
    if active_only:
        query = query.filter(Category.is_active == True)
    
    categories = query.order_by(Category.sort_order, Category.name).offset(skip).limit(limit).all()
    return categories


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new menu category"""
    # Check if category name already exists
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if new name conflicts with existing category
    if category_update.name and category_update.name != category.name:
        existing = db.query(Category).filter(Category.name == category_update.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category name already exists")
    
    # Update category
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}", response_model=MessageResponse)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has menu items
    menu_items_count = db.query(MenuItem).filter(MenuItem.category_id == category_id).count()
    if menu_items_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category with {menu_items_count} menu items"
        )
    
    db.delete(category)
    db.commit()
    return MessageResponse(message="Category deleted successfully")


# Menu Item endpoints
@router.get("/items", response_model=List[MenuItemResponse])
async def get_menu_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    available_only: bool = Query(True, description="Return only available items"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: Session = Depends(get_db)
):
    """Get menu items with filtering options"""
    query = db.query(MenuItem)
    
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    
    if category_id:
        query = query.filter(MenuItem.category_id == category_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (MenuItem.name.ilike(search_term)) |
            (MenuItem.description.ilike(search_term))
        )
    
    items = query.order_by(MenuItem.sort_order, MenuItem.name).offset(skip).limit(limit).all()
    return items


@router.post("/items", response_model=MenuItemResponse, status_code=201)
async def create_menu_item(
    item: MenuItemCreate,
    db: Session = Depends(get_db)
):
    """Create a new menu item"""
    # Verify category exists
    category = db.query(Category).filter(Category.id == item.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    
    # Check if item name already exists in the same category
    existing = db.query(MenuItem).filter(
        MenuItem.name == item.name,
        MenuItem.category_id == item.category_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Menu item with this name already exists in this category")
    
    db_item = MenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific menu item by ID"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.put("/items/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    item_update: MenuItemUpdate,
    db: Session = Depends(get_db)
):
    """Update a menu item"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Verify category exists if being updated
    if item_update.category_id:
        category = db.query(Category).filter(Category.id == item_update.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    # Check for name conflicts if name is being updated
    if item_update.name and item_update.name != item.name:
        category_id = item_update.category_id or item.category_id
        existing = db.query(MenuItem).filter(
            MenuItem.name == item_update.name,
            MenuItem.category_id == category_id,
            MenuItem.id != item_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Menu item with this name already exists in this category")
    
    # Update item
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}", response_model=MessageResponse)
async def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a menu item"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    db.delete(item)
    db.commit()
    return MessageResponse(message="Menu item deleted successfully")


@router.patch("/items/{item_id}/availability", response_model=MenuItemResponse)
async def toggle_item_availability(
    item_id: int,
    available: bool = Query(..., description="Set item availability"),
    db: Session = Depends(get_db)
):
    """Toggle menu item availability"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    item.is_available = available
    db.commit()
    db.refresh(item)
    return item


@router.get("/categories/{category_id}/items", response_model=List[MenuItemResponse])
async def get_category_items(
    category_id: int,
    available_only: bool = Query(True, description="Return only available items"),
    db: Session = Depends(get_db)
):
    """Get all menu items for a specific category"""
    # Verify category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    query = db.query(MenuItem).filter(MenuItem.category_id == category_id)
    
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    
    items = query.order_by(MenuItem.sort_order, MenuItem.name).all()
    return items