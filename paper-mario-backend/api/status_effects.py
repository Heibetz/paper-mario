"""Status Effect endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from config import get_db
from models import StatusEffect, CharacterStatusEffect
from models.status_effects import EffectType
from schemas.status_effects import (
    StatusEffectCreate, StatusEffectResponse, StatusEffectUpdate,
    CharacterStatusEffectCreate, CharacterStatusEffectResponse
)

router = APIRouter(prefix="/status-effects", tags=["Status Effects"])


@router.get("/", response_model=List[StatusEffectResponse])
def get_status_effects(
    skip: int = 0,
    limit: int = None,
    effect_type: Optional[EffectType] = Query(None, description="Filter by effect type"),
    db: Session = Depends(get_db)
):
    """Get all status effects with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(StatusEffect)
    
    if effect_type:
        query = query.filter(StatusEffect.effect_type == effect_type)
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    effects = query.all()
    return effects


@router.get("/{status_id}", response_model=StatusEffectResponse)
def get_status_effect(status_id: int, db: Session = Depends(get_db)):
    """Get a specific status effect by ID."""
    effect = db.query(StatusEffect).filter(StatusEffect.status_id == status_id).first()
    if not effect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Status effect with id {status_id} not found"
        )
    return effect


@router.post("/", response_model=StatusEffectResponse, status_code=status.HTTP_201_CREATED)
def create_status_effect(effect: StatusEffectCreate, db: Session = Depends(get_db)):
    """Create a new status effect."""
    # Check if status effect name already exists
    existing = db.query(StatusEffect).filter(StatusEffect.name == effect.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status effect with name '{effect.name}' already exists"
        )
    
    db_effect = StatusEffect(**effect.model_dump())
    db.add(db_effect)
    db.commit()
    db.refresh(db_effect)
    return db_effect


@router.put("/{status_id}", response_model=StatusEffectResponse)
def update_status_effect(
    status_id: int,
    effect_update: StatusEffectUpdate,
    db: Session = Depends(get_db)
):
    """Update a status effect."""
    db_effect = db.query(StatusEffect).filter(StatusEffect.status_id == status_id).first()
    if not db_effect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Status effect with id {status_id} not found"
        )
    
    update_data = effect_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_effect, field, value)
    
    db.commit()
    db.refresh(db_effect)
    return db_effect


@router.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status_effect(status_id: int, db: Session = Depends(get_db)):
    """Delete a status effect."""
    db_effect = db.query(StatusEffect).filter(StatusEffect.status_id == status_id).first()
    if not db_effect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Status effect with id {status_id} not found"
        )
    
    db.delete(db_effect)
    db.commit()
    return None


# Character Status Effect endpoints
@router.post("/apply", response_model=CharacterStatusEffectResponse, status_code=status.HTTP_201_CREATED)
def apply_status_to_character(
    char_status: CharacterStatusEffectCreate,
    db: Session = Depends(get_db)
):
    """Apply a status effect to a character."""
    db_char_status = CharacterStatusEffect(
        **char_status.model_dump(),
        applied_at=datetime.utcnow()
    )
    db.add(db_char_status)
    db.commit()
    db.refresh(db_char_status)
    return db_char_status


@router.get("/character/{character_id}", response_model=List[CharacterStatusEffectResponse])
def get_character_status_effects(character_id: int, db: Session = Depends(get_db)):
    """Get all status effects for a specific character."""
    effects = db.query(CharacterStatusEffect).filter(
        CharacterStatusEffect.character_id == character_id
    ).all()
    return effects
