"""Pixl model."""
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from config import Base


class Pixl(Base):
    """Pixl companions in the game."""
    
    __tablename__ = "pixls"
    
    # Primary Key
    pixl_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Columns
    name = Column(String(50), nullable=False, unique=True)  # UNIQUE constraint
    
    # Foreign Keys
    unlock_chapter_id = Column(
        Integer,
        ForeignKey("chapters.chapter_id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Columns
    ability = Column(Text)
    is_optional = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    unlock_chapter = relationship("Chapter", back_populates="pixls")
    
    # Indexes
    __table_args__ = (
        Index("idx_pixl_unlock_chapter", "unlock_chapter_id"),  # INDEX on FK
        Index("idx_pixl_name", "name"),  # INDEX on name
    )
    
    def __repr__(self):
        return f"<Pixl(id={self.pixl_id}, name='{self.name}', optional={self.is_optional})>"
