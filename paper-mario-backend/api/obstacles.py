"""Obstacle endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import Obstacle
from schemas.obstacles import ObstacleCreate, ObstacleResponse, ObstacleUpdate

router = APIRouter(prefix="/obstacles", tags=["Obstacles"])


@router.get("/", response_model=List[ObstacleResponse])
def get_obstacles(
    skip: int = 0,
    limit: int = None,
    location_id: Optional[int] = Query(None, description="Filter by location"),
    obstacle_type: Optional[str] = Query(None, description="Filter by obstacle type"),
    db: Session = Depends(get_db)
):
    """Get all obstacles with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(Obstacle)
    
    if location_id:
        query = query.filter(Obstacle.location_id == location_id)
    if obstacle_type:
        query = query.filter(Obstacle.type == obstacle_type)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    obstacles = query.all()
    return obstacles


@router.get("/{obstacle_id}", response_model=ObstacleResponse)
def get_obstacle(obstacle_id: int, db: Session = Depends(get_db)):
    """Get a specific obstacle by ID."""
    obstacle = db.query(Obstacle).filter(Obstacle.obstacle_id == obstacle_id).first()
    if not obstacle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Obstacle with id {obstacle_id} not found"
        )
    return obstacle


@router.post("/", response_model=ObstacleResponse, status_code=status.HTTP_201_CREATED)
def create_obstacle(obstacle: ObstacleCreate, db: Session = Depends(get_db)):
    """Create a new obstacle."""
    db_obstacle = Obstacle(**obstacle.model_dump())
    db.add(db_obstacle)
    db.commit()
    db.refresh(db_obstacle)
    return db_obstacle


@router.put("/{obstacle_id}", response_model=ObstacleResponse)
def update_obstacle(
    obstacle_id: int,
    obstacle_update: ObstacleUpdate,
    db: Session = Depends(get_db)
):
    """Update an obstacle."""
    db_obstacle = db.query(Obstacle).filter(Obstacle.obstacle_id == obstacle_id).first()
    if not db_obstacle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Obstacle with id {obstacle_id} not found"
        )
    
    update_data = obstacle_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obstacle, field, value)
    
    db.commit()
    db.refresh(db_obstacle)
    return db_obstacle


@router.delete("/{obstacle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_obstacle(obstacle_id: int, db: Session = Depends(get_db)):
    """Delete an obstacle."""
    db_obstacle = db.query(Obstacle).filter(Obstacle.obstacle_id == obstacle_id).first()
    if not db_obstacle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Obstacle with id {obstacle_id} not found"
        )
    
    db.delete(db_obstacle)
    db.commit()
    return None
