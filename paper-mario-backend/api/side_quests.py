"""Side Quest endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models import SideQuest
from schemas.side_quests import SideQuestCreate, SideQuestResponse, SideQuestUpdate

router = APIRouter(prefix="/side-quests", tags=["Side Quests"])


@router.get("/", response_model=List[SideQuestResponse])
def get_side_quests(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """Get all side quests. Use skip/limit for pagination (optional)."""
    query = db.query(SideQuest).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    quests = query.all()
    return quests


@router.get("/{quest_id}", response_model=SideQuestResponse)
def get_side_quest(quest_id: int, db: Session = Depends(get_db)):
    """Get a specific side quest by ID."""
    quest = db.query(SideQuest).filter(SideQuest.quest_id == quest_id).first()
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Side quest with id {quest_id} not found"
        )
    return quest


@router.post("/", response_model=SideQuestResponse, status_code=status.HTTP_201_CREATED)
def create_side_quest(quest: SideQuestCreate, db: Session = Depends(get_db)):
    """Create a new side quest."""
    # Check if quest name already exists
    existing = db.query(SideQuest).filter(SideQuest.name == quest.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Side quest with name '{quest.name}' already exists"
        )
    
    db_quest = SideQuest(**quest.model_dump())
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest


@router.put("/{quest_id}", response_model=SideQuestResponse)
def update_side_quest(
    quest_id: int,
    quest_update: SideQuestUpdate,
    db: Session = Depends(get_db)
):
    """Update a side quest."""
    db_quest = db.query(SideQuest).filter(SideQuest.quest_id == quest_id).first()
    if not db_quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Side quest with id {quest_id} not found"
        )
    
    # Update only provided fields
    update_data = quest_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_quest, field, value)
    
    db.commit()
    db.refresh(db_quest)
    return db_quest


@router.delete("/{quest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_side_quest(quest_id: int, db: Session = Depends(get_db)):
    """Delete a side quest."""
    db_quest = db.query(SideQuest).filter(SideQuest.quest_id == quest_id).first()
    if not db_quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Side quest with id {quest_id} not found"
        )
    
    db.delete(db_quest)
    db.commit()
    return None
