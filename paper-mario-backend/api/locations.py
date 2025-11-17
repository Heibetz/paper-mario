"""Location endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import Location
from models.locations import LocationType
from schemas.locations import LocationCreate, LocationResponse, LocationUpdate

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[LocationResponse])
def get_locations(
    skip: int = 0,
    limit: int = None,
    location_type: Optional[LocationType] = Query(None, description="Filter by location type"),
    chapter_id: Optional[int] = Query(None, description="Filter by chapter"),
    db: Session = Depends(get_db)
):
    """Get all locations with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(Location)
    
    if location_type:
        query = query.filter(Location.type == location_type)
    if chapter_id:
        query = query.filter(Location.chapter_id == chapter_id)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    locations = query.all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Get a specific location by ID."""
    location = db.query(Location).filter(Location.location_id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    return location


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    """Create a new location."""
    db_location = Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location_update: LocationUpdate,
    db: Session = Depends(get_db)
):
    """Update a location."""
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if not db_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    
    update_data = location_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_location, field, value)
    
    db.commit()
    db.refresh(db_location)
    return db_location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a location."""
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if not db_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    
    db.delete(db_location)
    db.commit()
    return None
