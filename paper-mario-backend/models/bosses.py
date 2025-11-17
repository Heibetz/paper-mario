"""Boss model."""
from sqlalchemy import Column, Integer, Text, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from config import Base


class Boss(Base):
    """Boss characters in the game."""
    
    __tablename__ = "bosses"
    
    # Primary Key
    boss_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    character_id = Column(
        Integer,
        ForeignKey("characters.character_id", ondelete="CASCADE"),
        nullable=False
    )
    chapter_id = Column(
        Integer,
        ForeignKey("chapters.chapter_id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Columns
    phase_count = Column(Integer, nullable=False, default=1)
    special_mechanics = Column(Text)
    
    # Relationships
    character = relationship("Character", back_populates="boss")
    chapter = relationship("Chapter", back_populates="bosses")
    
    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint("phase_count > 0", name="check_phase_count_positive"),  # CHECK constraint
        Index("idx_boss_character", "character_id"),  # INDEX on FK
        Index("idx_boss_chapter", "chapter_id"),  # INDEX on FK
    )
    
    def __repr__(self):
        return f"<Boss(id={self.boss_id}, phases={self.phase_count})>"
