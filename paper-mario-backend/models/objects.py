"""Object model."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from config import Base


class Object(Base):
    """Objects in game locations."""
    
    __tablename__ = "objects"
    
    # Primary Key
    object_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    location_id = Column(
        Integer,
        ForeignKey("locations.location_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Columns
    name = Column(String(100), nullable=False)
    object_type = Column(String(50), nullable=False)
    properties = Column(Text)
    
    # Relationships
    location = relationship("Location", back_populates="objects")
    
    # Indexes
    __table_args__ = (
        Index("idx_object_location", "location_id"),  # INDEX on FK
        Index("idx_object_type", "object_type"),  # INDEX on type for filtering
    )
    
    def __repr__(self):
        return f"<Object(id={self.object_id}, name='{self.name}', type='{self.object_type}')>"
