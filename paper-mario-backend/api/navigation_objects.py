"""Navigation Object endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import NavigationObject
from models.navigation_objects import NavigationType
from schemas.navigation_objects import NavigationObjectCreate, NavigationObjectResponse, NavigationObjectUpdate

router = APIRouter(prefix="/navigation-objects", tags=["Navigation Objects"])


@router.get("/", response_model=List[NavigationObjectResponse])
def get_navigation_objects(
    skip: int = 0,
    limit: int = None,
    location_id: Optional[int] = Query(None, description="Filter by location"),
    nav_type: Optional[NavigationType] = Query(None, description="Filter by navigation type"),
    db: Session = Depends(get_db)
):
    """Get all navigation objects with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(NavigationObject)
    
    if location_id:
        query = query.filter(NavigationObject.location_id == location_id)
    if nav_type:
        query = query.filter(NavigationObject.type == nav_type)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    nav_objects = query.all()
    return nav_objects


@router.get("/{navobj_id}", response_model=NavigationObjectResponse)
def get_navigation_object(navobj_id: int, db: Session = Depends(get_db)):
    """Get a specific navigation object by ID."""
    nav_obj = db.query(NavigationObject).filter(NavigationObject.navobj_id == navobj_id).first()
    if not nav_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Navigation object with id {navobj_id} not found"
        )
    return nav_obj


@router.post("/", response_model=NavigationObjectResponse, status_code=status.HTTP_201_CREATED)
def create_navigation_object(nav_obj: NavigationObjectCreate, db: Session = Depends(get_db)):
    """Create a new navigation object."""
    db_nav_obj = NavigationObject(**nav_obj.model_dump())
    db.add(db_nav_obj)
    db.commit()
    db.refresh(db_nav_obj)
    return db_nav_obj


@router.put("/{navobj_id}", response_model=NavigationObjectResponse)
def update_navigation_object(
    navobj_id: int,
    nav_obj_update: NavigationObjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a navigation object."""
    db_nav_obj = db.query(NavigationObject).filter(NavigationObject.navobj_id == navobj_id).first()
    if not db_nav_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Navigation object with id {navobj_id} not found"
        )
    
    update_data = nav_obj_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_nav_obj, field, value)
    
    db.commit()
    db.refresh(db_nav_obj)
    return db_nav_obj


@router.delete("/{navobj_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_navigation_object(navobj_id: int, db: Session = Depends(get_db)):
    """Delete a navigation object."""
    db_nav_obj = db.query(NavigationObject).filter(NavigationObject.navobj_id == navobj_id).first()
    if not db_nav_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Navigation object with id {navobj_id} not found"
        )
    
    db.delete(db_nav_obj)
    db.commit()
    return None
