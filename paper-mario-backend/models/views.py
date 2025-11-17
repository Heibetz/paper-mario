"""SQLAlchemy models for database views."""
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EnemyDetailsView(Base):
    """View for enemy details with character information."""
    __tablename__ = "enemy_details"
    __table_args__ = {'info': dict(is_view=True)}
    
    enemy_id = Column(Integer, primary_key=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    card_score = Column(Integer)
    character_id = Column(Integer)
    character_name = Column(String(100))
    description = Column(Text)


class BossDetailsView(Base):
    """View for boss details with character and chapter information."""
    __tablename__ = "boss_details"
    __table_args__ = {'info': dict(is_view=True)}
    
    boss_id = Column(Integer, primary_key=True)
    character_id = Column(Integer)
    chapter_id = Column(Integer)
    phase_count = Column(Integer)
    special_mechanics = Column(Text)
    boss_name = Column(String(100))
    boss_description = Column(Text)
    chapter_name = Column(String(100))
    world_number = Column(Integer)


class LocationSummaryView(Base):
    """View for location summary with chapter and object counts."""
    __tablename__ = "location_summary"
    __table_args__ = {'info': dict(is_view=True)}
    
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String(100))
    location_type = Column(String(50))
    description = Column(Text)
    chapter_id = Column(Integer)
    chapter_name = Column(String(100))
    world_number = Column(Integer)
    object_count = Column(Integer)
    block_count = Column(Integer)
    nav_object_count = Column(Integer)
    obstacle_count = Column(Integer)
    switch_count = Column(Integer)


class PlayableCharacterDetailsView(Base):
    """View for playable character details with unlock chapter."""
    __tablename__ = "playable_character_details"
    __table_args__ = {'info': dict(is_view=True)}
    
    character_id = Column(Integer, primary_key=True)
    character_name = Column(String(100))
    description = Column(Text)
    special_ability = Column(Text)
    unlock_chapter_id = Column(Integer)
    unlock_chapter_name = Column(String(100))
    unlock_world = Column(Integer)


class BlockInventoryView(Base):
    """View for block inventory with items and locations."""
    __tablename__ = "block_inventory"
    __table_args__ = {'info': dict(is_view=True)}
    
    block_id = Column(Integer, primary_key=True)
    block_type = Column(String(50))
    properties = Column(Text)
    location_id = Column(Integer)
    location_name = Column(String(100))
    location_type = Column(String(50))
    chapter_name = Column(String(100))
    world_number = Column(Integer)
    contains_item_id = Column(Integer)
    item_name = Column(String(100))
    is_key_item = Column(Boolean)
    item_effect = Column(Text)


class QuestOverviewView(Base):
    """View for quest overview with locations and rewards."""
    __tablename__ = "quest_overview"
    __table_args__ = {'info': dict(is_view=True)}
    
    quest_id = Column(Integer, primary_key=True)
    quest_name = Column(String(100))
    description = Column(Text)
    start_location_id = Column(Integer)
    start_location_name = Column(String(100))
    chapter_name = Column(String(100))
    reward_item_id = Column(Integer)
    reward_item_name = Column(String(100))
    reward_is_key_item = Column(Boolean)


class ChapterStatisticsView(Base):
    """View for chapter statistics with counts."""
    __tablename__ = "chapter_statistics"
    __table_args__ = {'info': dict(is_view=True)}
    
    chapter_id = Column(Integer, primary_key=True)
    chapter_name = Column(String(100))
    world_number = Column(Integer)
    description = Column(Text)
    location_count = Column(Integer)
    boss_count = Column(Integer)
    pixl_count = Column(Integer)
    playable_character_count = Column(Integer)
