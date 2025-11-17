"""Item model."""
from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from sqlalchemy.orm import relationship
from config import Base


class Item(Base):
    """Items in the game."""
    
    __tablename__ = "items"
    
    # Primary Key
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Columns
    name = Column(String(100), nullable=False, unique=True)  # UNIQUE constraint
    is_key_item = Column(Boolean, default=False, nullable=False)
    effect = Column(Text)
    
    # Relationships
    blocks = relationship("BlockContainer", back_populates="contains_item")
    side_quests = relationship("SideQuest", back_populates="reward_item")
    
    # Indexes
    __table_args__ = (
        Index("idx_item_name", "name"),  # INDEX on name
        Index("idx_item_key_item", "is_key_item"),  # INDEX for filtering key items
    )
    
    def __repr__(self):
        return f"<Item(id={self.item_id}, name='{self.name}', key_item={self.is_key_item})>"
