"""Obstacle model."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from config import Base


class Obstacle(Base):
    """Obstacles in game locations."""
    
    __tablename__ = "obstacles"
    
    # Primary Key
    obstacle_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    location_id = Column(
        Integer,
        ForeignKey("locations.location_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Columns
    type = Column(String(50), nullable=False)
    behavior = Column(Text)
    
    # Relationships
    location = relationship("Location", back_populates="obstacles")
    
    # Indexes
    __table_args__ = (
        Index("idx_obstacle_location", "location_id"),  # INDEX on FK
        Index("idx_obstacle_type", "type"),  # INDEX on type for filtering
    )
    
    def __repr__(self):
        return f"<Obstacle(id={self.obstacle_id}, type='{self.type}')>"
