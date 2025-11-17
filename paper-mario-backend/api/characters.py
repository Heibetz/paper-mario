"""Character endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models import Character
from schemas.characters import CharacterCreate, CharacterResponse, CharacterUpdate

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.get("/", response_model=List[CharacterResponse])
def get_characters(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """Get all characters. Use skip/limit for pagination (optional)."""
    query = db.query(Character).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    characters = query.all()
    return characters


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int, db: Session = Depends(get_db)):
    """Get a specific character by ID."""
    character = db.query(Character).filter(Character.character_id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
    return character


@router.post("/", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    """Create a new character."""
    # Check if character name already exists
    existing = db.query(Character).filter(Character.name == character.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Character with name '{character.name}' already exists"
        )
    
    db_character = Character(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(
    character_id: int,
    character_update: CharacterUpdate,
    db: Session = Depends(get_db)
):
    """Update a character."""
    db_character = db.query(Character).filter(Character.character_id == character_id).first()
    if not db_character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
    
    # Update only provided fields
    update_data = character_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_character, field, value)
    
    db.commit()
    db.refresh(db_character)
    return db_character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: int, db: Session = Depends(get_db)):
    """Delete a character."""
    db_character = db.query(Character).filter(Character.character_id == character_id).first()
    if not db_character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
    
    db.delete(db_character)
    db.commit()
    return None
