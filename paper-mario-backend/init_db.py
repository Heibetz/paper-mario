"""Initialize the database with all tables."""
from config import Base, engine
from models import (
    Character, PlayableCharacter, Chapter, Location, Pixl,
    StatusEffect, CharacterStatusEffect, Enemy, Boss, Item,
    Object, NavigationObject, Obstacle, BlockContainer, Switch,
    SideQuest, QuestCharacter
)


def init_database():
    """Create all tables in the database."""
    print("Creating database tables...")
    
    # Drop all tables (use with caution in production!)
    # Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✓ Database tables created successfully!")
    print("\nTables created:")
    print("  - characters")
    print("  - playable_characters")
    print("  - chapters")
    print("  - locations")
    print("  - pixls")
    print("  - status_effects")
    print("  - character_status_effects")
    print("  - enemies")
    print("  - bosses")
    print("  - items")
    print("  - objects")
    print("  - navigation_objects")
    print("  - obstacles")
    print("  - blocks_containers")
    print("  - switches")
    print("  - side_quests")
    print("  - quest_character")
    print("\n✓ All constraints and indexes have been applied!")


if __name__ == "__main__":
    init_database()
