"""Object schemas."""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ObjectBase(BaseModel):
    """Base object schema."""
    location_id: int
    name: str
    object_type: str
    properties: Optional[str] = None


class ObjectCreate(ObjectBase):
    """Schema for creating an object."""
    pass


class ObjectUpdate(BaseModel):
    """Schema for updating an object."""
    location_id: Optional[int] = None
    name: Optional[str] = None
    object_type: Optional[str] = None
    properties: Optional[str] = None


class ObjectResponse(ObjectBase):
    """Schema for object response."""
    object_id: int
    
    model_config = ConfigDict(from_attributes=True)
