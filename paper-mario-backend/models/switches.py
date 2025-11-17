"""Switch model."""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from config import Base


class Switch(Base):
    """Switches that control navigation objects."""
    
    __tablename__ = "switches"
    
    # Primary Key
    switch_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    location_id = Column(
        Integer,
        ForeignKey("locations.location_id", ondelete="CASCADE"),
        nullable=False
    )
    target_navobj_id = Column(
        Integer,
        ForeignKey("navigation_objects.navobj_id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Columns
    switch_type = Column(String(50), nullable=False)
    
    # Relationships
    location = relationship("Location", back_populates="switches")
    target_navobj = relationship("NavigationObject", back_populates="switches")
    
    # Indexes
    __table_args__ = (
        Index("idx_switch_location", "location_id"),  # INDEX on FK
        Index("idx_switch_target", "target_navobj_id"),  # INDEX on FK
        Index("idx_switch_type", "switch_type"),  # INDEX on type for filtering
    )
    
    def __repr__(self):
        return f"<Switch(id={self.switch_id}, type='{self.switch_type}')>"
