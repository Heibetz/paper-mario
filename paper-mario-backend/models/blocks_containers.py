"""Block/Container model."""
from sqlalchemy import Column, Integer, Text, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from config import Base
import enum


class BlockType(enum.Enum):
    """Block type enumeration."""
    movable = "movable"
    breakable = "breakable"
    save = "save"
    star = "star"


class BlockContainer(Base):
    """Blocks and containers in the game."""
    
    __tablename__ = "blocks_containers"
    
    # Primary Key
    block_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    location_id = Column(
        Integer,
        ForeignKey("locations.location_id", ondelete="CASCADE"),
        nullable=False
    )
    contains_item_id = Column(
        Integer,
        ForeignKey("items.item_id", ondelete="SET NULL"),
        nullable=True  # Nullable - not all blocks contain items
    )
    
    # Columns
    block_type = Column(Enum(BlockType), nullable=False)
    properties = Column(Text)
    
    # Relationships
    location = relationship("Location", back_populates="blocks")
    contains_item = relationship("Item", back_populates="blocks")
    
    # Indexes
    __table_args__ = (
        Index("idx_block_location", "location_id"),  # INDEX on FK
        Index("idx_block_item", "contains_item_id"),  # INDEX on FK
        Index("idx_block_type", "block_type"),  # INDEX on type for filtering
    )
    
    def __repr__(self):
        return f"<BlockContainer(id={self.block_id}, type={self.block_type.value})>"
