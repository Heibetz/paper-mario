"""Enemy endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import Enemy, Character
from schemas.enemies import EnemyCreate, EnemyResponse, EnemyUpdate

router = APIRouter(prefix="/enemies", tags=["Enemies"])


@router.get("/", response_model=List[EnemyResponse])
def get_enemies(
    skip: int = 0,
    limit: int = None,
    min_hp: Optional[int] = Query(None, description="Minimum HP filter"),
    max_hp: Optional[int] = Query(None, description="Maximum HP filter"),
    db: Session = Depends(get_db)
):
    """Get all enemies with optional HP filtering. Use skip/limit for pagination (optional)."""
    query = db.query(Enemy)
    
    if min_hp is not None:
        query = query.filter(Enemy.hp >= min_hp)
    if max_hp is not None:
        query = query.filter(Enemy.hp <= max_hp)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    enemies = query.all()
    return enemies


@router.get("/{enemy_id}", response_model=EnemyResponse)
def get_enemy(enemy_id: int, db: Session = Depends(get_db)):
    """Get a specific enemy by ID."""
    enemy = db.query(Enemy).filter(Enemy.enemy_id == enemy_id).first()
    if not enemy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enemy with id {enemy_id} not found"
        )
    return enemy


@router.get("/{enemy_id}/character")
def get_enemy_character(enemy_id: int, db: Session = Depends(get_db)):
    """Get the character info for a specific enemy."""
    enemy = db.query(Enemy).filter(Enemy.enemy_id == enemy_id).first()
    if not enemy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enemy with id {enemy_id} not found"
        )
    
    character = db.query(Character).filter(Character.character_id == enemy.character_id).first()
    return character


@router.post("/", response_model=EnemyResponse, status_code=status.HTTP_201_CREATED)
def create_enemy(enemy: EnemyCreate, db: Session = Depends(get_db)):
    """Create a new enemy."""
    # Check if character exists
    character = db.query(Character).filter(Character.character_id == enemy.character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {enemy.character_id} not found"
        )
    
    db_enemy = Enemy(**enemy.model_dump())
    db.add(db_enemy)
    db.commit()
    db.refresh(db_enemy)
    return db_enemy


@router.put("/{enemy_id}", response_model=EnemyResponse)
def update_enemy(
    enemy_id: int,
    enemy_update: EnemyUpdate,
    db: Session = Depends(get_db)
):
    """Update an enemy's stats."""
    db_enemy = db.query(Enemy).filter(Enemy.enemy_id == enemy_id).first()
    if not db_enemy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enemy with id {enemy_id} not found"
        )
    
    # Update only provided fields
    update_data = enemy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_enemy, field, value)
    
    db.commit()
    db.refresh(db_enemy)
    return db_enemy


@router.delete("/{enemy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enemy(enemy_id: int, db: Session = Depends(get_db)):
    """Delete an enemy."""
    db_enemy = db.query(Enemy).filter(Enemy.enemy_id == enemy_id).first()
    if not db_enemy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enemy with id {enemy_id} not found"
        )
    
    db.delete(db_enemy)
    db.commit()
    return None
