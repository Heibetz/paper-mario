"""Side Quest schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class SideQuestBase(BaseModel):
    """Base side quest schema."""
    name: str
    description: Optional[str] = None
    start_location_id: Optional[int] = None
    reward_item_id: Optional[int] = None


class SideQuestCreate(SideQuestBase):
    """Schema for creating a side quest."""
    pass


class SideQuestUpdate(BaseModel):
    """Schema for updating a side quest."""
    name: Optional[str] = None
    description: Optional[str] = None
    start_location_id: Optional[int] = None
    reward_item_id: Optional[int] = None


class SideQuestResponse(SideQuestBase):
    """Schema for side quest response."""
    quest_id: int
    
    model_config = ConfigDict(from_attributes=True)
