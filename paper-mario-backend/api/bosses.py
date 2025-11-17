"""Boss endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import Boss, Character
from schemas.bosses import BossCreate, BossResponse, BossUpdate

router = APIRouter(prefix="/bosses", tags=["Bosses"])


@router.get("/", response_model=List[BossResponse])
def get_bosses(
    skip: int = 0,
    limit: int = None,
    chapter_id: Optional[int] = Query(None, description="Filter by chapter"),
    db: Session = Depends(get_db)
):
    """Get all bosses with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(Boss)
    
    if chapter_id:
        query = query.filter(Boss.chapter_id == chapter_id)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    bosses = query.all()
    return bosses


@router.get("/{boss_id}", response_model=BossResponse)
def get_boss(boss_id: int, db: Session = Depends(get_db)):
    """Get a specific boss by ID."""
    boss = db.query(Boss).filter(Boss.boss_id == boss_id).first()
    if not boss:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Boss with id {boss_id} not found"
        )
    return boss


@router.get("/{boss_id}/character")
def get_boss_character(boss_id: int, db: Session = Depends(get_db)):
    """Get the character info for a specific boss."""
    boss = db.query(Boss).filter(Boss.boss_id == boss_id).first()
    if not boss:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Boss with id {boss_id} not found"
        )
    
    character = db.query(Character).filter(Character.character_id == boss.character_id).first()
    return character


@router.post("/", response_model=BossResponse, status_code=status.HTTP_201_CREATED)
def create_boss(boss: BossCreate, db: Session = Depends(get_db)):
    """Create a new boss."""
    # Check if character exists
    character = db.query(Character).filter(Character.character_id == boss.character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {boss.character_id} not found"
        )
    
    db_boss = Boss(**boss.model_dump())
    db.add(db_boss)
    db.commit()
    db.refresh(db_boss)
    return db_boss


@router.put("/{boss_id}", response_model=BossResponse)
def update_boss(
    boss_id: int,
    boss_update: BossUpdate,
    db: Session = Depends(get_db)
):
    """Update a boss."""
    db_boss = db.query(Boss).filter(Boss.boss_id == boss_id).first()
    if not db_boss:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Boss with id {boss_id} not found"
        )
    
    update_data = boss_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_boss, field, value)
    
    db.commit()
    db.refresh(db_boss)
    return db_boss


@router.delete("/{boss_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_boss(boss_id: int, db: Session = Depends(get_db)):
    """Delete a boss."""
    db_boss = db.query(Boss).filter(Boss.boss_id == boss_id).first()
    if not db_boss:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Boss with id {boss_id} not found"
        )
    
    db.delete(db_boss)
    db.commit()
    return None
