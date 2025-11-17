"""Chapter endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models import Chapter, Location
from schemas.chapters import ChapterCreate, ChapterResponse, ChapterUpdate

router = APIRouter(prefix="/chapters", tags=["Chapters"])


@router.get("/", response_model=List[ChapterResponse])
def get_chapters(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """Get all chapters. Use skip/limit for pagination (optional)."""
    query = db.query(Chapter).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    chapters = query.all()
    return chapters


@router.get("/{chapter_id}", response_model=ChapterResponse)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    """Get a specific chapter by ID."""
    chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter with id {chapter_id} not found"
        )
    return chapter


@router.get("/{chapter_id}/locations")
def get_chapter_locations(chapter_id: int, db: Session = Depends(get_db)):
    """Get all locations in a specific chapter."""
    chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter with id {chapter_id} not found"
        )
    
    locations = db.query(Location).filter(Location.chapter_id == chapter_id).all()
    return locations


@router.post("/", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db)):
    """Create a new chapter."""
    # Check if chapter name already exists
    existing = db.query(Chapter).filter(Chapter.name == chapter.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Chapter with name '{chapter.name}' already exists"
        )
    
    db_chapter = Chapter(**chapter.model_dump())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


@router.put("/{chapter_id}", response_model=ChapterResponse)
def update_chapter(
    chapter_id: int,
    chapter_update: ChapterUpdate,
    db: Session = Depends(get_db)
):
    """Update a chapter."""
    db_chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    if not db_chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter with id {chapter_id} not found"
        )
    
    # Update only provided fields
    update_data = chapter_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_chapter, field, value)
    
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


@router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    """Delete a chapter."""
    db_chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    if not db_chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter with id {chapter_id} not found"
        )
    
    db.delete(db_chapter)
    db.commit()
    return None
