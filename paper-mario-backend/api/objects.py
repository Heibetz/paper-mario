"""Object endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import Object
from schemas.objects import ObjectCreate, ObjectResponse, ObjectUpdate

router = APIRouter(prefix="/objects", tags=["Objects"])


@router.get("/", response_model=List[ObjectResponse])
def get_objects(
    skip: int = 0,
    limit: int = None,
    location_id: Optional[int] = Query(None, description="Filter by location"),
    object_type: Optional[str] = Query(None, description="Filter by object type"),
    db: Session = Depends(get_db)
):
    """Get all objects with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(Object)
    
    if location_id:
        query = query.filter(Object.location_id == location_id)
    if object_type:
        query = query.filter(Object.object_type == object_type)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    objects = query.all()
    return objects


@router.get("/{object_id}", response_model=ObjectResponse)
def get_object(object_id: int, db: Session = Depends(get_db)):
    """Get a specific object by ID."""
    obj = db.query(Object).filter(Object.object_id == object_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with id {object_id} not found"
        )
    return obj


@router.post("/", response_model=ObjectResponse, status_code=status.HTTP_201_CREATED)
def create_object(obj: ObjectCreate, db: Session = Depends(get_db)):
    """Create a new object."""
    db_object = Object(**obj.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


@router.put("/{object_id}", response_model=ObjectResponse)
def update_object(
    object_id: int,
    object_update: ObjectUpdate,
    db: Session = Depends(get_db)
):
    """Update an object."""
    db_object = db.query(Object).filter(Object.object_id == object_id).first()
    if not db_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with id {object_id} not found"
        )
    
    update_data = object_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_object, field, value)
    
    db.commit()
    db.refresh(db_object)
    return db_object


@router.delete("/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_object(object_id: int, db: Session = Depends(get_db)):
    """Delete an object."""
    db_object = db.query(Object).filter(Object.object_id == object_id).first()
    if not db_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with id {object_id} not found"
        )
    
    db.delete(db_object)
    db.commit()
    return None
