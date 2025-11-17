"""API endpoints for database views."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models.views import (
    EnemyDetailsView, BossDetailsView, LocationSummaryView,
    PlayableCharacterDetailsView, BlockInventoryView,
    QuestOverviewView, ChapterStatisticsView
)
from schemas.views import (
    EnemyDetailsResponse, BossDetailsResponse, LocationSummaryResponse,
    PlayableCharacterDetailsResponse, BlockInventoryResponse,
    QuestOverviewResponse, ChapterStatisticsResponse
)

router = APIRouter(prefix="/views", tags=["Database Views"])


@router.get("/enemy-details", response_model=List[EnemyDetailsResponse])
def get_enemy_details(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get enemy details from view.
    Pre-computed join of Enemies and Characters tables.
    """
    query = db.query(EnemyDetailsView).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@router.get("/boss-details", response_model=List[BossDetailsResponse])
def get_boss_details(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get boss details from view.
    Pre-computed join of Bosses, Characters, and Chapters tables.
    """
    query = db.query(BossDetailsView).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@router.get("/location-summary", response_model=List[LocationSummaryResponse])
def get_location_summary(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get location summary from view.
    Includes chapter info and counts of all objects/blocks/obstacles.
    """
    query = db.query(LocationSummaryView).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@router.get("/playable-character-details", response_model=List[PlayableCharacterDetailsResponse])
def get_playable_character_details(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get playable character details from view.
    Pre-computed join with unlock chapter information.
    """
    query = db.query(PlayableCharacterDetailsView).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@router.get("/block-inventory", response_model=List[BlockInventoryResponse])
def get_block_inventory(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get block inventory from view.
    Shows all blocks with their items and location details.
    """
    query = db.query(BlockInventoryView).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@router.get("/quest-overview", response_model=List[QuestOverviewResponse])
def get_quest_overview(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get quest overview from view.
    Shows side quests with location and reward information.
    """
    query = db.query(QuestOverviewView).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@router.get("/chapter-statistics", response_model=List[ChapterStatisticsResponse])
def get_chapter_statistics(
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get chapter statistics from view.
    Shows counts of locations, bosses, pixls, and playable characters per chapter.
    """
    query = db.query(ChapterStatisticsView).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@router.get("/chapter-statistics/{chapter_id}", response_model=ChapterStatisticsResponse)
def get_chapter_statistics_by_id(chapter_id: int, db: Session = Depends(get_db)):
    """Get statistics for a specific chapter from view."""
    result = db.query(ChapterStatisticsView).filter(
        ChapterStatisticsView.chapter_id == chapter_id
    ).first()
    
    if not result:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter {chapter_id} not found"
        )
    
    return result
