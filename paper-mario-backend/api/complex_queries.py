"""Complex query endpoints with multiple joins."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from config import get_db
from models import (
    Enemy, Character, Boss, Chapter, Location,
    BlockContainer, Item, SideQuest, PlayableCharacter,
    QuestCharacter
)

router = APIRouter(prefix="/queries", tags=["Complex Queries"])


@router.get("/enemies-with-details")
def get_enemies_with_details(db: Session = Depends(get_db)):
    """
    Get all enemies with their character information.
    Joins: Enemy -> Character
    """
    results = db.query(
        Enemy.enemy_id,
        Enemy.hp,
        Enemy.attack,
        Enemy.defense,
        Enemy.card_score,
        Character.name.label("character_name"),
        Character.description.label("character_description")
    ).join(
        Character, Enemy.character_id == Character.character_id
    ).all()
    
    return [
        {
            "enemy_id": r.enemy_id,
            "hp": r.hp,
            "attack": r.attack,
            "defense": r.defense,
            "card_score": r.card_score,
            "character_name": r.character_name,
            "character_description": r.character_description
        }
        for r in results
    ]


@router.get("/bosses-with-details")
def get_bosses_with_details(db: Session = Depends(get_db)):
    """
    Get all bosses with character and chapter information.
    Joins: Boss -> Character, Boss -> Chapter
    """
    results = db.query(
        Boss.boss_id,
        Boss.phase_count,
        Boss.special_mechanics,
        Character.name.label("character_name"),
        Character.description.label("character_description"),
        Chapter.name.label("chapter_name"),
        Chapter.world_number
    ).join(
        Character, Boss.character_id == Character.character_id
    ).join(
        Chapter, Boss.chapter_id == Chapter.chapter_id
    ).all()
    
    return [
        {
            "boss_id": r.boss_id,
            "boss_name": r.character_name,
            "description": r.character_description,
            "phase_count": r.phase_count,
            "special_mechanics": r.special_mechanics,
            "chapter": r.chapter_name,
            "world_number": r.world_number
        }
        for r in results
    ]


@router.get("/playable-characters-with-chapters")
def get_playable_characters_with_chapters(db: Session = Depends(get_db)):
    """
    Get playable characters with their unlock chapter details.
    Joins: PlayableCharacter -> Character, PlayableCharacter -> Chapter (left join)
    """
    results = db.query(
        PlayableCharacter.character_id,
        Character.name.label("character_name"),
        Character.description,
        PlayableCharacter.special_ability,
        Chapter.name.label("unlock_chapter"),
        Chapter.world_number
    ).join(
        Character, PlayableCharacter.character_id == Character.character_id
    ).outerjoin(  # Left join since unlock_chapter can be NULL
        Chapter, PlayableCharacter.unlock_chapter_id == Chapter.chapter_id
    ).all()
    
    return [
        {
            "character_id": r.character_id,
            "name": r.character_name,
            "description": r.description,
            "special_ability": r.special_ability,
            "unlock_chapter": r.unlock_chapter,
            "unlock_world": r.world_number
        }
        for r in results
    ]


@router.get("/blocks-with-items-and-locations")
def get_blocks_with_items_and_locations(db: Session = Depends(get_db)):
    """
    Get blocks with their contained items and location details.
    Joins: BlockContainer -> Item (left join), BlockContainer -> Location -> Chapter
    """
    results = db.query(
        BlockContainer.block_id,
        BlockContainer.block_type,
        BlockContainer.properties.label("block_properties"),
        Item.name.label("item_name"),
        Item.is_key_item,
        Location.name.label("location_name"),
        Location.type.label("location_type"),
        Chapter.name.label("chapter_name"),
        Chapter.world_number
    ).outerjoin(  # Left join - blocks may not contain items
        Item, BlockContainer.contains_item_id == Item.item_id
    ).join(
        Location, BlockContainer.location_id == Location.location_id
    ).join(
        Chapter, Location.chapter_id == Chapter.chapter_id
    ).all()
    
    return [
        {
            "block_id": r.block_id,
            "block_type": r.block_type,
            "properties": r.block_properties,
            "contains_item": r.item_name,
            "is_key_item": r.is_key_item,
            "location": r.location_name,
            "location_type": r.location_type,
            "chapter": r.chapter_name,
            "world": r.world_number
        }
        for r in results
    ]


@router.get("/side-quests-full-details")
def get_side_quests_full_details(db: Session = Depends(get_db)):
    """
    Get side quests with location, reward item, and involved characters.
    Joins: SideQuest -> Location -> Chapter, SideQuest -> Item, SideQuest -> QuestCharacter -> Character
    """
    results = db.query(
        SideQuest.quest_id,
        SideQuest.name.label("quest_name"),
        SideQuest.description,
        Location.name.label("start_location"),
        Chapter.name.label("chapter"),
        Item.name.label("reward"),
        Character.name.label("character_name"),
        QuestCharacter.role
    ).outerjoin(
        Location, SideQuest.start_location_id == Location.location_id
    ).outerjoin(
        Chapter, Location.chapter_id == Chapter.chapter_id
    ).outerjoin(
        Item, SideQuest.reward_item_id == Item.item_id
    ).outerjoin(
        QuestCharacter, SideQuest.quest_id == QuestCharacter.quest_id
    ).outerjoin(
        Character, QuestCharacter.character_id == Character.character_id
    ).all()
    
    # Group by quest_id to handle multiple characters per quest
    quests_dict = {}
    for r in results:
        if r.quest_id not in quests_dict:
            quests_dict[r.quest_id] = {
                "quest_id": r.quest_id,
                "name": r.quest_name,
                "description": r.description,
                "start_location": r.start_location,
                "chapter": r.chapter,
                "reward": r.reward,
                "characters": []
            }
        
        if r.character_name:
            quests_dict[r.quest_id]["characters"].append({
                "name": r.character_name,
                "role": r.role.value if r.role else None
            })
    
    return list(quests_dict.values())


@router.get("/locations-with-everything")
def get_locations_with_everything(db: Session = Depends(get_db)):
    """
    Get locations with chapter info and count of objects, enemies, blocks, etc.
    Complex aggregation query with multiple joins.
    """
    from sqlalchemy import func
    from models import Object, NavigationObject, Obstacle, Switch
    
    results = db.query(
        Location.location_id,
        Location.name.label("location_name"),
        Location.type.label("location_type"),
        Location.description,
        Chapter.name.label("chapter_name"),
        Chapter.world_number,
        func.count(Object.object_id.distinct()).label("object_count"),
        func.count(BlockContainer.block_id.distinct()).label("block_count"),
        func.count(NavigationObject.navobj_id.distinct()).label("nav_object_count"),
        func.count(Obstacle.obstacle_id.distinct()).label("obstacle_count"),
        func.count(Switch.switch_id.distinct()).label("switch_count")
    ).join(
        Chapter, Location.chapter_id == Chapter.chapter_id
    ).outerjoin(
        Object, Location.location_id == Object.location_id
    ).outerjoin(
        BlockContainer, Location.location_id == BlockContainer.location_id
    ).outerjoin(
        NavigationObject, Location.location_id == NavigationObject.location_id
    ).outerjoin(
        Obstacle, Location.location_id == Obstacle.location_id
    ).outerjoin(
        Switch, Location.location_id == Switch.location_id
    ).group_by(
        Location.location_id,
        Location.name,
        Location.type,
        Location.description,
        Chapter.name,
        Chapter.world_number
    ).all()
    
    return [
        {
            "location_id": r.location_id,
            "name": r.location_name,
            "type": r.location_type,
            "description": r.description,
            "chapter": r.chapter_name,
            "world": r.world_number,
            "statistics": {
                "objects": r.object_count,
                "blocks": r.block_count,
                "navigation_objects": r.nav_object_count,
                "obstacles": r.obstacle_count,
                "switches": r.switch_count,
                "total_interactive_elements": (
                    r.object_count + r.block_count + r.nav_object_count + 
                    r.obstacle_count + r.switch_count
                )
            }
        }
        for r in results
    ]


@router.get("/chapter-summary/{chapter_id}")
def get_chapter_summary(chapter_id: int, db: Session = Depends(get_db)):
    """
    Get complete summary of a chapter with all related data.
    Multiple joins and aggregations.
    """
    from sqlalchemy import func
    from models import Pixl
    
    # Get chapter basic info
    chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    if not chapter:
        return {"error": "Chapter not found"}
    
    # Count locations
    location_count = db.query(func.count(Location.location_id)).filter(
        Location.chapter_id == chapter_id
    ).scalar()
    
    # Get bosses in this chapter
    bosses = db.query(
        Character.name,
        Boss.phase_count,
        Boss.special_mechanics
    ).join(
        Boss, Character.character_id == Boss.character_id
    ).filter(
        Boss.chapter_id == chapter_id
    ).all()
    
    # Get playable characters unlocked in this chapter
    playable_chars = db.query(
        Character.name,
        PlayableCharacter.special_ability
    ).join(
        PlayableCharacter, Character.character_id == PlayableCharacter.character_id
    ).filter(
        PlayableCharacter.unlock_chapter_id == chapter_id
    ).all()
    
    # Get pixls unlocked in this chapter
    pixls = db.query(Pixl).filter(Pixl.unlock_chapter_id == chapter_id).all()
    
    return {
        "chapter_id": chapter.chapter_id,
        "name": chapter.name,
        "world_number": chapter.world_number,
        "description": chapter.description,
        "statistics": {
            "location_count": location_count
        },
        "bosses": [
            {
                "name": b.name,
                "phase_count": b.phase_count,
                "special_mechanics": b.special_mechanics
            }
            for b in bosses
        ],
        "playable_characters_unlocked": [
            {
                "name": pc.name,
                "special_ability": pc.special_ability
            }
            for pc in playable_chars
        ],
        "pixls_unlocked": [
            {
                "name": p.name,
                "ability": p.ability,
                "is_optional": p.is_optional
            }
            for p in pixls
        ]
    }
