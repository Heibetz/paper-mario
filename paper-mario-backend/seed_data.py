"""Seed the database with sample Paper Mario data."""
from datetime import datetime, timedelta
from config import SessionLocal
from models import (
    Character, PlayableCharacter, Chapter, Location, Pixl,
    StatusEffect, CharacterStatusEffect, Enemy, Boss, Item,
    Object, NavigationObject, Obstacle, BlockContainer, Switch,
    SideQuest, QuestCharacter
)
from models.locations import LocationType
from models.status_effects import EffectType
from models.navigation_objects import NavigationType
from models.blocks_containers import BlockType
from models.side_quests import QuestRole


def seed_database():
    """Seed database with sample Super Paper Mario data."""
    db = SessionLocal()
    
    try:
        print("Seeding database with sample data...")
        
        # Create Chapters
        print("\n→ Creating Chapters...")
        chapter1 = Chapter(name="Lineland", world_number=1, description="A flat, 2D world")
        chapter2 = Chapter(name="Gloam Valley", world_number=2, description="A mysterious valley")
        chapter3 = Chapter(name="The Bitlands", world_number=3, description="A pixelated world")
        db.add_all([chapter1, chapter2, chapter3])
        db.commit()
        print(f"  ✓ Created {db.query(Chapter).count()} chapters")
        
        # Create Characters
        print("\n→ Creating Characters...")
        mario = Character(name="Mario", description="The hero in red")
        peach = Character(name="Princess Peach", description="Princess of the Mushroom Kingdom")
        bowser = Character(name="Bowser", description="King of the Koopas")
        luigi = Character(name="Luigi", description="Mario's brother in green")
        goomba = Character(name="Goomba", description="Common enemy")
        koopa = Character(name="Koopa Troopa", description="Turtle enemy")
        fracktail = Character(name="Fracktail", description="Chapter 1 boss")
        db.add_all([mario, peach, bowser, luigi, goomba, koopa, fracktail])
        db.commit()
        print(f"  ✓ Created {db.query(Character).count()} characters")
        
        # Create Playable Characters
        print("\n→ Creating Playable Characters...")
        playable_mario = PlayableCharacter(
            character_id=mario.character_id,
            unlock_chapter_id=chapter1.chapter_id,
            special_ability="Flip between dimensions"
        )
        playable_peach = PlayableCharacter(
            character_id=peach.character_id,
            unlock_chapter_id=chapter1.chapter_id,
            special_ability="Float with parasol"
        )
        playable_bowser = PlayableCharacter(
            character_id=bowser.character_id,
            unlock_chapter_id=chapter3.chapter_id,
            special_ability="Breathe fire"
        )
        db.add_all([playable_mario, playable_peach, playable_bowser])
        db.commit()
        print(f"  ✓ Created {db.query(PlayableCharacter).count()} playable characters")
        
        # Create Pixls
        print("\n→ Creating Pixls...")
        tippi = Pixl(
            name="Tippi",
            unlock_chapter_id=chapter1.chapter_id,
            ability="Point at hidden objects and enemies",
            is_optional=False
        )
        boomer = Pixl(
            name="Boomer",
            unlock_chapter_id=chapter1.chapter_id,
            ability="Throw bombs",
            is_optional=False
        )
        db.add_all([tippi, boomer])
        db.commit()
        print(f"  ✓ Created {db.query(Pixl).count()} pixls")
        
        # Create Locations
        print("\n→ Creating Locations...")
        flipside = Location(
            chapter_id=chapter1.chapter_id,
            name="Flipside",
            type=LocationType.hub,
            description="The main hub world between dimensions"
        )
        lineland_road = Location(
            chapter_id=chapter1.chapter_id,
            name="Lineland Road",
            type=LocationType.level,
            description="First level of Chapter 1"
        )
        yold_desert = Location(
            chapter_id=chapter1.chapter_id,
            name="Yold Desert",
            type=LocationType.dungeon,
            description="Desert area with puzzles"
        )
        db.add_all([flipside, lineland_road, yold_desert])
        db.commit()
        print(f"  ✓ Created {db.query(Location).count()} locations")
        
        # Create Enemies
        print("\n→ Creating Enemies...")
        enemy_goomba = Enemy(
            character_id=goomba.character_id,
            hp=10,
            attack=1,
            defense=0,
            card_score=5
        )
        enemy_koopa = Enemy(
            character_id=koopa.character_id,
            hp=15,
            attack=2,
            defense=1,
            card_score=10
        )
        db.add_all([enemy_goomba, enemy_koopa])
        db.commit()
        print(f"  ✓ Created {db.query(Enemy).count()} enemies")
        
        # Create Boss
        print("\n→ Creating Bosses...")
        boss_fracktail = Boss(
            character_id=fracktail.character_id,
            chapter_id=chapter1.chapter_id,
            phase_count=2,
            special_mechanics="Flying dragon with antenna weak points"
        )
        db.add(boss_fracktail)
        db.commit()
        print(f"  ✓ Created {db.query(Boss).count()} bosses")
        
        # Create Items
        print("\n→ Creating Items...")
        mushroom = Item(name="Mushroom", is_key_item=False, effect="Restores 10 HP")
        super_mushroom = Item(name="Super Mushroom", is_key_item=False, effect="Restores 25 HP")
        pure_heart = Item(name="Pure Heart", is_key_item=True, effect="Essential story item")
        db.add_all([mushroom, super_mushroom, pure_heart])
        db.commit()
        print(f"  ✓ Created {db.query(Item).count()} items")
        
        # Create Status Effects
        print("\n→ Creating Status Effects...")
        poison = StatusEffect(name="Poison", effect_type=EffectType.debuff, duration_seconds=30)
        mega_star = StatusEffect(name="Mega Star", effect_type=EffectType.buff, duration_seconds=20)
        db.add_all([poison, mega_star])
        db.commit()
        print(f"  ✓ Created {db.query(StatusEffect).count()} status effects")
        
        # Create Navigation Objects
        print("\n→ Creating Navigation Objects...")
        door = NavigationObject(
            location_id=flipside.location_id,
            type=NavigationType.door,
            properties="Leads to Chapter 1"
        )
        save_block = NavigationObject(
            location_id=flipside.location_id,
            type=NavigationType.save_block,
            properties="Save your progress"
        )
        db.add_all([door, save_block])
        db.commit()
        print(f"  ✓ Created {db.query(NavigationObject).count()} navigation objects")
        
        # Create Blocks
        print("\n→ Creating Blocks...")
        item_block = BlockContainer(
            location_id=lineland_road.location_id,
            block_type=BlockType.breakable,
            contains_item_id=mushroom.item_id,
            properties="Contains a mushroom"
        )
        save_block_container = BlockContainer(
            location_id=flipside.location_id,
            block_type=BlockType.save,
            contains_item_id=None,
            properties="Save block"
        )
        db.add_all([item_block, save_block_container])
        db.commit()
        print(f"  ✓ Created {db.query(BlockContainer).count()} blocks")
        
        # Create Obstacles
        print("\n→ Creating Obstacles...")
        spike_trap = Obstacle(
            location_id=yold_desert.location_id,
            type="Spikes",
            behavior="Damages player on contact"
        )
        db.add(spike_trap)
        db.commit()
        print(f"  ✓ Created {db.query(Obstacle).count()} obstacles")
        
        # Create Objects
        print("\n→ Creating Objects...")
        chest = Object(
            location_id=yold_desert.location_id,
            name="Treasure Chest",
            object_type="container",
            properties="Contains rare items"
        )
        db.add(chest)
        db.commit()
        print(f"  ✓ Created {db.query(Object).count()} objects")
        
        # Create Switches
        print("\n→ Creating Switches...")
        red_switch = Switch(
            location_id=yold_desert.location_id,
            switch_type="pressure_plate",
            target_navobj_id=door.navobj_id
        )
        db.add(red_switch)
        db.commit()
        print(f"  ✓ Created {db.query(Switch).count()} switches")
        
        # Create Side Quest
        print("\n→ Creating Side Quests...")
        sidequest1 = SideQuest(
            name="Find Luigi",
            description="Rescue Luigi from his predicament",
            start_location_id=flipside.location_id,
            reward_item_id=super_mushroom.item_id
        )
        db.add(sidequest1)
        db.commit()
        print(f"  ✓ Created {db.query(SideQuest).count()} side quests")
        
        # Create Quest Character relationship
        print("\n→ Creating Quest-Character relationships...")
        quest_char = QuestCharacter(
            quest_id=sidequest1.quest_id,
            character_id=luigi.character_id,
            role=QuestRole.target
        )
        db.add(quest_char)
        db.commit()
        print(f"  ✓ Created {db.query(QuestCharacter).count()} quest-character relationships")
        
        # Create Character Status Effect
        print("\n→ Creating Character Status Effects...")
        mario_poisoned = CharacterStatusEffect(
            character_id=mario.character_id,
            status_id=poison.status_id,
            applied_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(seconds=30)
        )
        db.add(mario_poisoned)
        db.commit()
        print(f"  ✓ Created {db.query(CharacterStatusEffect).count()} character status effects")
        
        print("\n" + "="*60)
        print("✓ Database seeded successfully with sample data!")
        print("="*60)
        
        # Print summary
        print("\n📊 Database Summary:")
        print(f"  • Characters: {db.query(Character).count()}")
        print(f"  • Playable Characters: {db.query(PlayableCharacter).count()}")
        print(f"  • Chapters: {db.query(Chapter).count()}")
        print(f"  • Locations: {db.query(Location).count()}")
        print(f"  • Pixls: {db.query(Pixl).count()}")
        print(f"  • Enemies: {db.query(Enemy).count()}")
        print(f"  • Bosses: {db.query(Boss).count()}")
        print(f"  • Items: {db.query(Item).count()}")
        print(f"  • Status Effects: {db.query(StatusEffect).count()}")
        print(f"  • Navigation Objects: {db.query(NavigationObject).count()}")
        print(f"  • Blocks: {db.query(BlockContainer).count()}")
        print(f"  • Obstacles: {db.query(Obstacle).count()}")
        print(f"  • Objects: {db.query(Object).count()}")
        print(f"  • Switches: {db.query(Switch).count()}")
        print(f"  • Side Quests: {db.query(SideQuest).count()}")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
