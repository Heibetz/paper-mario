"""Switch schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class SwitchBase(BaseModel):
    """Base switch schema."""
    location_id: int
    switch_type: str
    target_navobj_id: Optional[int] = None


class SwitchCreate(SwitchBase):
    """Schema for creating a switch."""
    pass


class SwitchUpdate(BaseModel):
    """Schema for updating a switch."""
    location_id: Optional[int] = None
    switch_type: Optional[str] = None
    target_navobj_id: Optional[int] = None


class SwitchResponse(SwitchBase):
    """Schema for switch response."""
    switch_id: int
    
    model_config = ConfigDict(from_attributes=True)
