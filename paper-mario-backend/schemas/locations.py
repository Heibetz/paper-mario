"""Location schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from models.locations import LocationType


class LocationBase(BaseModel):
    """Base location schema."""
    chapter_id: int
    name: str
    type: LocationType
    description: Optional[str] = None


class LocationCreate(LocationBase):
    """Schema for creating a location."""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating a location."""
    chapter_id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[LocationType] = None
    description: Optional[str] = None


class LocationResponse(LocationBase):
    """Schema for location response."""
    location_id: int
    
    model_config = ConfigDict(from_attributes=True)
