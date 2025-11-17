"""Block Container schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from models.blocks_containers import BlockType


class BlockContainerBase(BaseModel):
    """Base block container schema."""
    location_id: int
    block_type: BlockType
    contains_item_id: Optional[int] = None
    properties: Optional[str] = None


class BlockContainerCreate(BlockContainerBase):
    """Schema for creating a block container."""
    pass


class BlockContainerUpdate(BaseModel):
    """Schema for updating a block container."""
    location_id: Optional[int] = None
    block_type: Optional[BlockType] = None
    contains_item_id: Optional[int] = None
    properties: Optional[str] = None


class BlockContainerResponse(BlockContainerBase):
    """Schema for block container response."""
    block_id: int
    
    model_config = ConfigDict(from_attributes=True)
