"""Create database views for common queries."""
from sqlalchemy import text
from config import engine

def create_views():
    """Create SQL views for common complex queries."""
    
    with engine.connect() as conn:
        
        # View 1: Enemy Details (Enemy + Character info)
        conn.execute(text("""
            DROP VIEW IF EXISTS enemy_details
        """))
        conn.execute(text("""
            CREATE VIEW enemy_details AS
            SELECT 
                e.enemy_id,
                e.hp,
                e.attack,
                e.defense,
                e.card_score,
                c.character_id,
                c.name AS character_name,
                c.description
            FROM enemies e
            JOIN characters c ON e.character_id = c.character_id
        """))
        print("✓ Created view: enemy_details")
        
        # View 2: Boss Details (Boss + Character + Chapter info)
        conn.execute(text("""
            DROP VIEW IF EXISTS boss_details
        """))
        conn.execute(text("""
            CREATE VIEW boss_details AS
            SELECT 
                b.boss_id,
                b.character_id,
                b.chapter_id,
                b.phase_count,
                b.special_mechanics,
                c.name AS boss_name,
                c.description AS boss_description,
                ch.name AS chapter_name,
                ch.world_number
            FROM bosses b
            JOIN characters c ON b.character_id = c.character_id
            JOIN chapters ch ON b.chapter_id = ch.chapter_id
        """))
        print("✓ Created view: boss_details")
        
        # View 3: Location Summary (Location + Chapter + counts)
        conn.execute(text("""
            DROP VIEW IF EXISTS location_summary
        """))
        conn.execute(text("""
            CREATE VIEW location_summary AS
            SELECT 
                l.location_id,
                l.name AS location_name,
                l.type AS location_type,
                l.description,
                l.chapter_id,
                ch.name AS chapter_name,
                ch.world_number,
                (SELECT COUNT(*) FROM objects WHERE location_id = l.location_id) AS object_count,
                (SELECT COUNT(*) FROM blocks_containers WHERE location_id = l.location_id) AS block_count,
                (SELECT COUNT(*) FROM navigation_objects WHERE location_id = l.location_id) AS nav_object_count,
                (SELECT COUNT(*) FROM obstacles WHERE location_id = l.location_id) AS obstacle_count,
                (SELECT COUNT(*) FROM switches WHERE location_id = l.location_id) AS switch_count
            FROM locations l
            JOIN chapters ch ON l.chapter_id = ch.chapter_id
        """))
        print("✓ Created view: location_summary")
        
        # View 4: Playable Character Full Info
        conn.execute(text("""
            DROP VIEW IF EXISTS playable_character_details
        """))
        conn.execute(text("""
            CREATE VIEW playable_character_details AS
            SELECT 
                pc.character_id,
                c.name AS character_name,
                c.description,
                pc.special_ability,
                pc.unlock_chapter_id,
                ch.name AS unlock_chapter_name,
                ch.world_number AS unlock_world
            FROM playable_characters pc
            JOIN characters c ON pc.character_id = c.character_id
            LEFT JOIN chapters ch ON pc.unlock_chapter_id = ch.chapter_id
        """))
        print("✓ Created view: playable_character_details")
        
        # View 5: Block Inventory (Blocks with items and locations)
        conn.execute(text("""
            DROP VIEW IF EXISTS block_inventory
        """))
        conn.execute(text("""
            CREATE VIEW block_inventory AS
            SELECT 
                bc.block_id,
                bc.block_type,
                bc.properties,
                bc.location_id,
                l.name AS location_name,
                l.type AS location_type,
                ch.name AS chapter_name,
                ch.world_number,
                bc.contains_item_id,
                i.name AS item_name,
                i.is_key_item,
                i.effect AS item_effect
            FROM blocks_containers bc
            JOIN locations l ON bc.location_id = l.location_id
            JOIN chapters ch ON l.chapter_id = ch.chapter_id
            LEFT JOIN items i ON bc.contains_item_id = i.item_id
        """))
        print("✓ Created view: block_inventory")
        
        # View 6: Quest Overview (Side quests with all related info)
        conn.execute(text("""
            DROP VIEW IF EXISTS quest_overview
        """))
        conn.execute(text("""
            CREATE VIEW quest_overview AS
            SELECT 
                sq.quest_id,
                sq.name AS quest_name,
                sq.description,
                sq.start_location_id,
                l.name AS start_location_name,
                ch.name AS chapter_name,
                sq.reward_item_id,
                i.name AS reward_item_name,
                i.is_key_item AS reward_is_key_item
            FROM side_quests sq
            LEFT JOIN locations l ON sq.start_location_id = l.location_id
            LEFT JOIN chapters ch ON l.chapter_id = ch.chapter_id
            LEFT JOIN items i ON sq.reward_item_id = i.item_id
        """))
        print("✓ Created view: quest_overview")
        
        # View 7: Chapter Statistics
        conn.execute(text("""
            DROP VIEW IF EXISTS chapter_statistics
        """))
        conn.execute(text("""
            CREATE VIEW chapter_statistics AS
            SELECT 
                ch.chapter_id,
                ch.name AS chapter_name,
                ch.world_number,
                ch.description,
                (SELECT COUNT(*) FROM locations WHERE chapter_id = ch.chapter_id) AS location_count,
                (SELECT COUNT(*) FROM bosses WHERE chapter_id = ch.chapter_id) AS boss_count,
                (SELECT COUNT(*) FROM pixls WHERE unlock_chapter_id = ch.chapter_id) AS pixl_count,
                (SELECT COUNT(*) FROM playable_characters WHERE unlock_chapter_id = ch.chapter_id) AS playable_character_count
            FROM chapters ch
        """))
        print("✓ Created view: chapter_statistics")
        
        conn.commit()
        print("\n✅ All views created successfully!")

if __name__ == "__main__":
    print("Creating database views...\n")
    create_views()
