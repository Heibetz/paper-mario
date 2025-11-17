"""API endpoints for stored procedures."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional

from config import get_db
from stored_procedures import StoredProcedures

router = APIRouter(prefix="/procedures", tags=["Stored Procedures"])


# Request schemas
class CreateEnemyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    hp: int = Field(..., gt=0)
    attack: int = Field(..., ge=0)
    defense: int = Field(..., ge=0)
    card_score: int = Field(..., gt=0)


class CreateBossRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    chapter_id: int
    phase_count: int = Field(..., gt=0)
    special_mechanics: Optional[str] = None


class CreateQuestRequest(BaseModel):
    quest_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    start_location_id: Optional[int] = None
    reward_item_id: Optional[int] = None
    quest_giver_id: Optional[int] = None
    quest_target_id: Optional[int] = None
    quest_helper_ids: Optional[List[int]] = None


class ApplyStatusEffectRequest(BaseModel):
    character_id: int
    status_id: int
    duration_seconds: int = Field(..., gt=0)


class BlockConfig(BaseModel):
    block_type: str
    contains_item_id: Optional[int] = None
    properties: Optional[str] = None


class PopulateLocationRequest(BaseModel):
    location_id: int
    blocks: List[BlockConfig]


class TransferItemRequest(BaseModel):
    from_block_id: int
    to_block_id: int


# Endpoints
@router.post("/create-enemy")
def create_enemy_with_character(
    request: CreateEnemyRequest,
    db: Session = Depends(get_db)
):
    """
    Stored Procedure: Create an enemy with its character in one transaction.
    
    This ensures data consistency - if either the character or enemy creation fails,
    neither will be saved to the database.
    """
    result = StoredProcedures.create_enemy_with_character(
        db=db,
        name=request.name,
        description=request.description,
        hp=request.hp,
        attack=request.attack,
        defense=request.defense,
        card_score=request.card_score
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to create enemy")
        )
    
    return result


@router.post("/create-boss")
def create_boss_with_character(
    request: CreateBossRequest,
    db: Session = Depends(get_db)
):
    """
    Stored Procedure: Create a boss with its character in one transaction.
    
    Validates chapter existence and creates both character and boss records atomically.
    """
    result = StoredProcedures.create_boss_with_character(
        db=db,
        name=request.name,
        description=request.description,
        chapter_id=request.chapter_id,
        phase_count=request.phase_count,
        special_mechanics=request.special_mechanics
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to create boss")
        )
    
    return result


@router.post("/create-quest")
def create_side_quest_with_characters(
    request: CreateQuestRequest,
    db: Session = Depends(get_db)
):
    """
    Stored Procedure: Create a side quest with all related characters in one transaction.
    
    Creates the quest and assigns giver, target, and helper characters atomically.
    """
    result = StoredProcedures.create_side_quest_with_characters(
        db=db,
        quest_name=request.quest_name,
        description=request.description,
        start_location_id=request.start_location_id,
        reward_item_id=request.reward_item_id,
        quest_giver_id=request.quest_giver_id,
        quest_target_id=request.quest_target_id,
        quest_helper_ids=request.quest_helper_ids
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to create quest")
        )
    
    return result


@router.post("/apply-status-effect")
def apply_status_effect(
    request: ApplyStatusEffectRequest,
    db: Session = Depends(get_db)
):
    """
    Stored Procedure: Apply a status effect to a character.
    
    Handles checking if effect is already applied and updates or creates accordingly.
    """
    result = StoredProcedures.apply_status_effect_to_character(
        db=db,
        character_id=request.character_id,
        status_id=request.status_id,
        duration_seconds=request.duration_seconds
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to apply status effect")
        )
    
    return result


@router.post("/populate-location")
def populate_location_with_blocks(
    request: PopulateLocationRequest,
    db: Session = Depends(get_db)
):
    """
    Stored Procedure: Populate a location with multiple blocks at once.
    
    Creates all blocks in a single transaction - all succeed or all fail.
    """
    block_configs = [block.dict() for block in request.blocks]
    
    result = StoredProcedures.populate_location_with_blocks(
        db=db,
        location_id=request.location_id,
        block_configs=block_configs
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to populate location")
        )
    
    return result


@router.get("/chapter-info/{chapter_id}")
def get_chapter_complete_info(chapter_id: int, db: Session = Depends(get_db)):
    """
    Stored Procedure: Get complete chapter information.
    
    Returns all related data (locations, bosses, pixls, playable characters) in one call.
    """
    result = StoredProcedures.get_chapter_complete_info(db, chapter_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("error", "Chapter not found")
        )
    
    return result


@router.post("/transfer-item")
def transfer_item_between_blocks(
    request: TransferItemRequest,
    db: Session = Depends(get_db)
):
    """
    Stored Procedure: Transfer an item from one block to another.
    
    Atomically moves an item between two blocks in a single transaction.
    """
    result = StoredProcedures.transfer_item_between_blocks(
        db=db,
        from_block_id=request.from_block_id,
        to_block_id=request.to_block_id
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to transfer item")
        )
    
    return result
