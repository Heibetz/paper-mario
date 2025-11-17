"""Pixl endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import Pixl
from schemas.pixls import PixlCreate, PixlResponse, PixlUpdate

router = APIRouter(prefix="/pixls", tags=["Pixls"])


@router.get("/", response_model=List[PixlResponse])
def get_pixls(
    skip: int = 0,
    limit: int = None,
    optional_only: Optional[bool] = Query(None, description="Filter for optional pixls"),
    db: Session = Depends(get_db)
):
    """Get all pixls with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(Pixl)
    
    if optional_only is not None:
        query = query.filter(Pixl.is_optional == optional_only)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    pixls = query.all()
    return pixls


@router.get("/{pixl_id}", response_model=PixlResponse)
def get_pixl(pixl_id: int, db: Session = Depends(get_db)):
    """Get a specific pixl by ID."""
    pixl = db.query(Pixl).filter(Pixl.pixl_id == pixl_id).first()
    if not pixl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pixl with id {pixl_id} not found"
        )
    return pixl


@router.post("/", response_model=PixlResponse, status_code=status.HTTP_201_CREATED)
def create_pixl(pixl: PixlCreate, db: Session = Depends(get_db)):
    """Create a new pixl."""
    # Check if pixl name already exists
    existing = db.query(Pixl).filter(Pixl.name == pixl.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pixl with name '{pixl.name}' already exists"
        )
    
    db_pixl = Pixl(**pixl.model_dump())
    db.add(db_pixl)
    db.commit()
    db.refresh(db_pixl)
    return db_pixl


@router.put("/{pixl_id}", response_model=PixlResponse)
def update_pixl(
    pixl_id: int,
    pixl_update: PixlUpdate,
    db: Session = Depends(get_db)
):
    """Update a pixl."""
    db_pixl = db.query(Pixl).filter(Pixl.pixl_id == pixl_id).first()
    if not db_pixl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pixl with id {pixl_id} not found"
        )
    
    update_data = pixl_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pixl, field, value)
    
    db.commit()
    db.refresh(db_pixl)
    return db_pixl


@router.delete("/{pixl_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pixl(pixl_id: int, db: Session = Depends(get_db)):
    """Delete a pixl."""
    db_pixl = db.query(Pixl).filter(Pixl.pixl_id == pixl_id).first()
    if not db_pixl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pixl with id {pixl_id} not found"
        )
    
    db.delete(db_pixl)
    db.commit()
    return None
