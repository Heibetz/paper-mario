"""Item schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ItemBase(BaseModel):
    """Base item schema."""
    name: str
    is_key_item: bool = False
    effect: Optional[str] = None


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""
    name: Optional[str] = None
    is_key_item: Optional[bool] = None
    effect: Optional[str] = None


class ItemResponse(ItemBase):
    """Schema for item response."""
    item_id: int
    
    model_config = ConfigDict(from_attributes=True)
