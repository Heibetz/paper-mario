"""Block Container endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config import get_db
from models import BlockContainer
from models.blocks_containers import BlockType
from schemas.blocks_containers import BlockContainerCreate, BlockContainerResponse, BlockContainerUpdate

router = APIRouter(prefix="/blocks", tags=["Blocks & Containers"])


@router.get("/", response_model=List[BlockContainerResponse])
def get_blocks(
    skip: int = 0,
    limit: int = None,
    location_id: Optional[int] = Query(None, description="Filter by location"),
    block_type: Optional[BlockType] = Query(None, description="Filter by block type"),
    has_item: Optional[bool] = Query(None, description="Filter blocks that contain items"),
    db: Session = Depends(get_db)
):
    """Get all blocks with optional filtering. Use skip/limit for pagination (optional)."""
    query = db.query(BlockContainer)
    
    if location_id:
        query = query.filter(BlockContainer.location_id == location_id)
    if block_type:
        query = query.filter(BlockContainer.block_type == block_type)
    if has_item is not None:
        if has_item:
            query = query.filter(BlockContainer.contains_item_id.isnot(None))
        else:
            query = query.filter(BlockContainer.contains_item_id.is_(None))
    
    query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    blocks = query.all()
    return blocks


@router.get("/{block_id}", response_model=BlockContainerResponse)
def get_block(block_id: int, db: Session = Depends(get_db)):
    """Get a specific block by ID."""
    block = db.query(BlockContainer).filter(BlockContainer.block_id == block_id).first()
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block with id {block_id} not found"
        )
    return block


@router.post("/", response_model=BlockContainerResponse, status_code=status.HTTP_201_CREATED)
def create_block(block: BlockContainerCreate, db: Session = Depends(get_db)):
    """Create a new block."""
    db_block = BlockContainer(**block.model_dump())
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block


@router.put("/{block_id}", response_model=BlockContainerResponse)
def update_block(
    block_id: int,
    block_update: BlockContainerUpdate,
    db: Session = Depends(get_db)
):
    """Update a block."""
    db_block = db.query(BlockContainer).filter(BlockContainer.block_id == block_id).first()
    if not db_block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block with id {block_id} not found"
        )
    
    update_data = block_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_block, field, value)
    
    db.commit()
    db.refresh(db_block)
    return db_block


@router.delete("/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_block(block_id: int, db: Session = Depends(get_db)):
    """Delete a block."""
    db_block = db.query(BlockContainer).filter(BlockContainer.block_id == block_id).first()
    if not db_block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block with id {block_id} not found"
        )
    
    db.delete(db_block)
    db.commit()
    return None
