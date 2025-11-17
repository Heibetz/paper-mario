"""Playable Character endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models import PlayableCharacter, Character
from schemas.playable_characters import PlayableCharacterCreate, PlayableCharacterResponse, PlayableCharacterUpdate

router = APIRouter(prefix="/playable-characters", tags=["Playable Characters"])


@router.get("/", response_model=List[PlayableCharacterResponse])
def get_playable_characters(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """Get all playable characters. Use skip/limit for pagination (optional)."""
    query = db.query(PlayableCharacter).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    playable_chars = query.all()
    return playable_chars


@router.get("/{character_id}", response_model=PlayableCharacterResponse)
def get_playable_character(character_id: int, db: Session = Depends(get_db)):
    """Get a specific playable character by ID."""
    playable = db.query(PlayableCharacter).filter(
        PlayableCharacter.character_id == character_id
    ).first()
    if not playable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Playable character with id {character_id} not found"
        )
    return playable


@router.post("/", response_model=PlayableCharacterResponse, status_code=status.HTTP_201_CREATED)
def create_playable_character(playable: PlayableCharacterCreate, db: Session = Depends(get_db)):
    """Create a new playable character."""
    # Check if character exists
    character = db.query(Character).filter(
        Character.character_id == playable.character_id
    ).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {playable.character_id} not found"
        )
    
    # Check if already exists as playable
    existing = db.query(PlayableCharacter).filter(
        PlayableCharacter.character_id == playable.character_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Character {playable.character_id} is already playable"
        )
    
    db_playable = PlayableCharacter(**playable.model_dump())
    db.add(db_playable)
    db.commit()
    db.refresh(db_playable)
    return db_playable


@router.put("/{character_id}", response_model=PlayableCharacterResponse)
def update_playable_character(
    character_id: int,
    playable_update: PlayableCharacterUpdate,
    db: Session = Depends(get_db)
):
    """Update a playable character."""
    db_playable = db.query(PlayableCharacter).filter(
        PlayableCharacter.character_id == character_id
    ).first()
    if not db_playable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Playable character with id {character_id} not found"
        )
    
    update_data = playable_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_playable, field, value)
    
    db.commit()
    db.refresh(db_playable)
    return db_playable


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playable_character(character_id: int, db: Session = Depends(get_db)):
    """Delete a playable character."""
    db_playable = db.query(PlayableCharacter).filter(
        PlayableCharacter.character_id == character_id
    ).first()
    if not db_playable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Playable character with id {character_id} not found"
        )
    
    db.delete(db_playable)
    db.commit()
    return None
