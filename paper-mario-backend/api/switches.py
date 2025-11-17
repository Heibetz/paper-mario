"""Switch endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import Switch
from schemas.switches import SwitchCreate, SwitchResponse, SwitchUpdate

router = APIRouter(prefix="/switches", tags=["Switches"])


@router.get("/", response_model=List[SwitchResponse])
def get_switches(
    skip: int = 0,
    limit: int = None,
    location_id: Optional[int] = Query(None, description="Filter by location"),
    switch_type: Optional[str] = Query(None, description="Filter by switch type"),
    db: Session = Depends(get_db)
):
    """Get all switches with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(Switch)
    
    if location_id:
        query = query.filter(Switch.location_id == location_id)
    if switch_type:
        query = query.filter(Switch.switch_type == switch_type)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    switches = query.all()
    return switches


@router.get("/{switch_id}", response_model=SwitchResponse)
def get_switch(switch_id: int, db: Session = Depends(get_db)):
    """Get a specific switch by ID."""
    switch = db.query(Switch).filter(Switch.switch_id == switch_id).first()
    if not switch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Switch with id {switch_id} not found"
        )
    return switch


@router.post("/", response_model=SwitchResponse, status_code=status.HTTP_201_CREATED)
def create_switch(switch: SwitchCreate, db: Session = Depends(get_db)):
    """Create a new switch."""
    db_switch = Switch(**switch.model_dump())
    db.add(db_switch)
    db.commit()
    db.refresh(db_switch)
    return db_switch


@router.put("/{switch_id}", response_model=SwitchResponse)
def update_switch(
    switch_id: int,
    switch_update: SwitchUpdate,
    db: Session = Depends(get_db)
):
    """Update a switch."""
    db_switch = db.query(Switch).filter(Switch.switch_id == switch_id).first()
    if not db_switch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Switch with id {switch_id} not found"
        )
    
    update_data = switch_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_switch, field, value)
    
    db.commit()
    db.refresh(db_switch)
    return db_switch


@router.delete("/{switch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_switch(switch_id: int, db: Session = Depends(get_db)):
    """Delete a switch."""
    db_switch = db.query(Switch).filter(Switch.switch_id == switch_id).first()
    if not db_switch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Switch with id {switch_id} not found"
        )
    
    db.delete(db_switch)
    db.commit()
    return None
