"""Comprehensive seed data from Super Paper Mario wiki."""
from datetime import datetime, timedelta
from config import SessionLocal
from models import (
    Chapter, Character, PlayableCharacter, Location, Pixl,
    StatusEffect, CharacterStatusEffect, Enemy, Boss, Item,
    Object, NavigationObject, Obstacle, BlockContainer, Switch,
    SideQuest, QuestCharacter
)
from models.locations import LocationType
from models.navigation_objects import NavigationType
from models.blocks_containers import BlockType
from models.status_effects import EffectType
from models.side_quests import QuestRole


def seed_comprehensive():
    """Seed with comprehensive Super Paper Mario data from wiki."""
    db = SessionLocal()
    
    try:
        print("🎮 Seeding Super Paper Mario database with comprehensive data...\n")
        
        # ===== CHAPTERS =====
        print("📚 Creating All Chapters...")
        chapters_data = [
            ("Lineland", 1, "A flat 2D world with Yold Town, Yold Desert, and Yold Ruins"),
            ("Gloam Valley", 2, "A dark mysterious valley leading to Merlee's Mansion"),
            ("The Bitlands", 3, "A retro pixelated world with Fort Francis and Tile Pool"),
            ("Outer Space", 4, "Space adventure through Planet Blobule and the Whoa Zone"),
            ("Land of the Cragnons", 5, "Underground caverns with Floro Sapiens and Cragnons"),
            ("Sammer's Kingdom", 6, "World of 100 warriors, destroyed by the Void"),
            ("The Underwhere", 7, "The land of the dead with Underwhere and Overthere"),
            ("Castle Bleck", 8, "Count Bleck's fortress and final battleground"),
        ]
        
        chapters = []
        for name, world_num, desc in chapters_data:
            chapters.append(Chapter(name=name, world_number=world_num, description=desc))
        db.add_all(chapters)
        db.commit()
        print(f"  ✅ Created {len(chapters)} chapters\n")
        
        # ===== PLAYABLE CHARACTERS =====
        print("🎭 Creating Playable Characters...")
        char_data = [
            ("Mario", "The legendary hero who can flip between dimensions", "Flip between 2D and 3D", chapters[0].chapter_id),
            ("Princess Peach", "The fair and lovely princess who can float", "Float with her parasol", chapters[0].chapter_id),
            ("Bowser", "The furious monster king with fire breath", "Breathe fire to burn enemies", chapters[2].chapter_id),
            ("Luigi", "The man in green with super jump ability", "Super jump higher than others", chapters[6].chapter_id),
        ]
        
        characters = []
        playable_chars = []
        for name, desc, ability, unlock_ch in char_data:
            char = Character(name=name, description=desc)
            db.add(char)
            db.flush()
            pc = PlayableCharacter(character_id=char.character_id, special_ability=ability, unlock_chapter_id=unlock_ch)
            characters.append(char)
            playable_chars.append(pc)
        
        db.add_all(playable_chars)
        db.commit()
        print(f"  ✅ Created 4 playable characters\n")
        
        # ===== ALL PIXLS =====
        print("✨ Creating All Pixls...")
        pixls_data = [
            ("Tippi", "Tattle and reveal hidden objects", False, chapters[0].chapter_id),
            ("Thoreau", "Pick up and throw enemies and objects", False, chapters[0].chapter_id),
            ("Boomer", "Throw bombs to destroy blocks and enemies", False, chapters[1].chapter_id),
            ("Slim", "Become paper-thin to slip through bars", False, chapters[1].chapter_id),
            ("Thudley", "Ground pound to hit switches and break blocks", False, chapters[2].chapter_id),
            ("Carrie", "Ride on her to move faster and avoid spikes", False, chapters[3].chapter_id),
            ("Fleep", "Flip objects and enemies from background to foreground", False, chapters[3].chapter_id),
            ("Cudge", "Swing a hammer to smash yellow blocks", True, chapters[4].chapter_id),
            ("Dottie", "Shrink to squeeze through tiny spaces", True, chapters[4].chapter_id),
            ("Barry", "Create a protective barrier that reflects attacks", True, chapters[2].chapter_id),
            ("Dashell", "Run at super speed", True, None),  # Pit of 100 Trials reward
            ("Piccolo", "Play music to put enemies to sleep", True, None),  # Flopside sidequest
            ("Tiptron", "Replacement for Tippi with same abilities", False, None),  # Post-game
        ]
        
        pixls = []
        for name, ability, optional, unlock_ch in pixls_data:
            pixls.append(Pixl(name=name, ability=ability, is_optional=optional, unlock_chapter_id=unlock_ch))
        db.add_all(pixls)
        db.commit()
        print(f"  ✅ Created {len(pixls)} Pixls (4 optional)\n")
        
        # ===== ENEMIES =====
        print("👾 Creating Enemies...")
        enemy_chars = [
            ("Goomba", "Common mushroom enemy, one of Bowser's minions"),
            ("Koopa Troopa", "Turtle soldier with a shell"),
            ("Squiglet", "Small black squiggly creature"),
            ("Zombie Shroom", "Undead mushroom that can poison"),
            ("Cherbil", "Floating creature that spreads poison gas"),
            ("Hammer Bro", "Throws hammers from a distance"),
            ("Clubba", "Strong enemy with a large club"),
            ("Spike Top", "Spiky Koopa that can't be jumped on"),
            ("Buzzy Beetle", "Fire-proof beetle with hard shell"),
            ("Lakitu", "Cloud-riding Koopa who throws Spinies"),
            ("Spiny", "Red spiked enemy thrown by Lakitus"),
            ("Piranha Plant", "Plant enemy that bites"),
            ("Boo", "Shy ghost that stops when looked at"),
            ("Magikoopa", "Magic-using Koopa who shoots spells"),
            ("Blooper", "Squid enemy from underwater areas"),
        ]
        
        enemies = []
        for name, desc in enemy_chars:
            char = Character(name=name, description=desc)
            db.add(char)
            db.flush()
            hp = 1 if name in ["Goomba", "Squiglet"] else (2 if name in ["Koopa Troopa", "Boo"] else 5)
            attack = 1 if name in ["Goomba", "Squiglet", "Koopa Troopa"] else 2
            defense = 0 if name not in ["Buzzy Beetle", "Spike Top"] else 1
            enemy = Enemy(character_id=char.character_id, hp=hp, attack=attack, defense=defense, card_score=5)
            enemies.append(enemy)
        
        db.add_all(enemies)
        db.commit()
        print(f"  ✅ Created {len(enemies)} enemies\n")
        
        # ===== BOSSES =====
        print("👹 Creating All Bosses...")
        boss_data = [
            ("O'Chunks", "Count Bleck's loyal warrior", chapters[0].chapter_id, 1, "Charges and throws chunks"),
            ("Fracktail", "Robotic dragon guardian of the Pure Heart", chapters[0].chapter_id, 1, "Flying dragon with weak points on antenna"),
            ("Mimi", "Shape-shifting minion with spider form", chapters[1].chapter_id, 2, "Transform into spider and create rubees"),
            ("Dimentio", "Mysterious jester with dimension powers", chapters[2].chapter_id, 1, "Teleportation and magic box attacks"),
            ("Francis", "Nerdy chameleon who kidnapped Tippi", chapters[3].chapter_id, 1, "Nerdy insults and tech attacks"),
            ("Mr. L", "Brainwashed Luigi with robot Brobot", chapters[3].chapter_id, 1, "Pilots Brobot robot"),
            ("Big Blooper", "Giant squid boss of the Tile Pool", chapters[2].chapter_id, 1, "Ink spray and tentacle attacks"),
            ("King Croacus IV", "Floro Sapien king corrupted by pollution", chapters[4].chapter_id, 3, "Multi-phase plant boss"),
            ("Brobot L-Type", "Upgraded version of Mr. L's robot", chapters[5].chapter_id, 1, "Space battle with lasers"),
            ("Bonechill", "Frozen dragon lord of the Overthere", chapters[6].chapter_id, 1, "Ice breath and freeze attacks"),
            ("Count Bleck", "Main antagonist trying to destroy all worlds", chapters[7].chapter_id, 2, "Void magic and invincibility with Chaos Heart"),
            ("Super Dimentio", "Dimentio fused with Luigi and Chaos Heart", chapters[7].chapter_id, 1, "Final boss with invincibility, defeated by Pure Hearts"),
            ("Wracktail", "Optional dark version of Fracktail", chapters[0].chapter_id, 1, "Stronger Fracktail fought in Pit of 100 Trials"),
            ("Shadoo", "Dark being who transforms into heroes", chapters[0].chapter_id, 4, "Shapeshifts into dark versions of Mario, Peach, Bowser, Luigi"),
        ]
        
        bosses = []
        for name, desc, chapter_id, phases, mechanics in boss_data:
            char = Character(name=name, description=desc)
            db.add(char)
            db.flush()
            boss = Boss(character_id=char.character_id, chapter_id=chapter_id, phase_count=phases, special_mechanics=mechanics)
            bosses.append(boss)
        
        db.add_all(bosses)
        db.commit()
        print(f"  ✅ Created {len(bosses)} bosses\n")
        
        # ===== ITEMS =====
        print("🎁 Creating Items...")
        items_data = [
            ("Mushroom", "Restores 10 HP", False),
            ("Super Shroom", "Restores 20 HP", False),
            ("Ultra Shroom", "Restores 50 HP", False),
            ("Fire Burst", "Broils enemies with searing flames", False),
            ("Ice Storm", "Pelts enemies with frigid ice shards", False),
            ("Thunder Rage", "Strikes enemies with lightning", False),
            ("POW Block", "Rattles enemies on ground and ceiling", False),
            ("Ghost Shroom", "Summons ghost to damage enemies", False),
            ("Volt Shroom", "Paralyzes enemies on contact", False),
            ("Shell Shock", "Shell that rams into enemies", False),
            ("Shooting Star", "Showers enemies with stars", False),
            ("Block Block", "Makes player invincible temporarily", False),
            ("Courage Shell", "Reduces damage taken by half", False),
            ("Bone-In Cut", "Doubles attack power briefly", False),
            ("Hot Sauce", "Doubles attack temporarily", False),
            ("Mighty Tonic", "Doubles attack temporarily", False),
            ("Turtley Leaf", "Reduces damage by half temporarily", False),
            ("Poison Shroom", "Poisons the player - don't use!", False),
            ("Dangerous Delight", "Blocks abilities and reverses controls", False),
            ("Pure Heart", "Legendary heart needed to stop the Void", True),
            ("Catch Card", "Card containing soul of an enemy", False),
            ("Gold Bar", "Valuable item worth 100 coins", False),
            ("Gold Medal", "Rare valuable collectible", False),
            ("Flipside Token", "Currency for arcade games", False),
            ("Map", "Shows location of hidden treasure", True),
        ]
        
        items = []
        for name, effect, is_key in items_data:
            items.append(Item(name=name, effect=effect, is_key_item=is_key))
        db.add_all(items)
        db.commit()
        print(f"  ✅ Created {len(items)} items\n")
        
        # ===== LOCATIONS =====
        print("🗺️  Creating Locations...")
        locations_data = [
            # Chapter 1
            (chapters[0].chapter_id, "Flipside", LocationType.hub, "Main hub world between dimensions"),
            (chapters[0].chapter_id, "Lineland Road", LocationType.level, "First level, flat 2D road"),
            (chapters[0].chapter_id, "Mount Lineland", LocationType.level, "Mountain where Mario learns to flip"),
            (chapters[0].chapter_id, "Yold Town", LocationType.other, "Town of elderly residents"),
            (chapters[0].chapter_id, "Yold Desert", LocationType.level, "Puzzle desert with sand"),
            (chapters[0].chapter_id, "Yold Ruins", LocationType.dungeon, "Ancient ruins with Fracktail boss"),
            # Chapter 2
            (chapters[1].chapter_id, "Gloam Valley", LocationType.level, "Dark valley path"),
            (chapters[1].chapter_id, "Merlee's Mansion", LocationType.dungeon, "Mansion filled with Mimi's tricks"),
            (chapters[1].chapter_id, "Merlee's Basement", LocationType.dungeon, "Basement with Mimi boss fight"),
            # Chapter 3
            (chapters[2].chapter_id, "The Bitlands", LocationType.level, "Retro pixelated overworld"),
            (chapters[2].chapter_id, "The Tile Pool", LocationType.level, "Underwater area with Big Blooper"),
            (chapters[2].chapter_id, "The Dotwood Tree", LocationType.level, "Giant tree with Dimentio encounter"),
            (chapters[2].chapter_id, "Fort Francis", LocationType.dungeon, "Francis's nerdy fortress"),
            # Chapter 4
            (chapters[3].chapter_id, "Outer Space", LocationType.level, "Space with zero gravity"),
            (chapters[3].chapter_id, "Planet Blobule", LocationType.level, "Planet of blob creatures"),
            (chapters[3].chapter_id, "Outer Limits", LocationType.level, "Space station"),
            (chapters[3].chapter_id, "Whoa Zone", LocationType.dungeon, "Psychedelic dimension with Mr. L"),
            # Chapter 5
            (chapters[4].chapter_id, "Downtown of Crag", LocationType.other, "Cragnon village"),
            (chapters[4].chapter_id, "Gap of Crag", LocationType.level, "Canyon area"),
            (chapters[4].chapter_id, "Floro Caverns", LocationType.dungeon, "Underground Floro Sapien caves"),
            # Chapter 6
            (chapters[5].chapter_id, "Sammer's Kingdom", LocationType.level, "World of 100 warriors"),
            (chapters[5].chapter_id, "World of Nothing", LocationType.level, "Void-destroyed wasteland"),
            # Chapter 7
            (chapters[6].chapter_id, "The Underwhere", LocationType.dungeon, "Land of the dead"),
            (chapters[6].chapter_id, "Underwhere Road", LocationType.level, "Path through Underwhere"),
            (chapters[6].chapter_id, "Overthere Stair", LocationType.level, "Long stairway to heaven"),
            (chapters[6].chapter_id, "The Overthere", LocationType.dungeon, "Heaven with Bonechill"),
            # Chapter 8
            (chapters[7].chapter_id, "Castle Bleck Entry", LocationType.dungeon, "Castle entrance"),
            (chapters[7].chapter_id, "Castle Bleck Foyer", LocationType.dungeon, "Main hall"),
            (chapters[7].chapter_id, "Castle Bleck Interior", LocationType.dungeon, "Inner areas"),
            (chapters[7].chapter_id, "Castle Bleck Inner Sanctum", LocationType.dungeon, "Final battle arena"),
            # Special
            (chapters[0].chapter_id, "Flopside", LocationType.hub, "Mirror dimension of Flipside"),
            (chapters[0].chapter_id, "Flipside Pit of 100 Trials", LocationType.dungeon, "100-floor challenge dungeon"),
            (chapters[0].chapter_id, "Flopside Pit of 100 Trials", LocationType.dungeon, "Dark version with Shadoo"),
        ]
        
        locations = []
        for chapter_id, name, loc_type, desc in locations_data:
            locations.append(Location(chapter_id=chapter_id, name=name, type=loc_type, description=desc))
        db.add_all(locations)
        db.commit()
        print(f"  ✅ Created {len(locations)} locations\n")
        
        # ===== STATUS EFFECTS =====
        print("💫 Creating Status Effects...")
        status_data = [
            ("Poisoned", EffectType.debuff, 30),
            ("Frozen", EffectType.debuff, 10),
            ("Stunned", EffectType.debuff, 5),
            ("Burned", EffectType.debuff, 15),
            ("Electrified", EffectType.buff, 20),
            ("Invincible", EffectType.buff, 10),
            ("Attack Up", EffectType.buff, 30),
            ("Defense Up", EffectType.buff, 30),
            ("Slow", EffectType.debuff, 20),
            ("Sleep", EffectType.debuff, 15),
        ]
        
        statuses = []
        for name, effect_type, duration in status_data:
            statuses.append(StatusEffect(name=name, effect_type=effect_type, duration_seconds=duration))
        db.add_all(statuses)
        db.commit()
        print(f"  ✅ Created {len(statuses)} status effects\n")
        
        # ===== SIDE QUESTS =====
        print("📜 Creating Side Quests...")
        quests_data = [
            ("Duel of 100", "Fight through 100 warriors in Sammer's Kingdom", locations[20].location_id, None),
            ("Flipside Pit Challenge", "Descend 100 floors to face Wracktail", locations[31].location_id, items[19].item_id),
            ("Flopside Pit Challenge", "Defeat Shadoo at floor 100", locations[32].location_id, items[20].item_id),
            ("Find Missing Pixls", "Locate all optional Pixls", locations[0].location_id, None),
            ("Arcade Master", "Win all arcade games", locations[0].location_id, items[23].item_id),
            ("Recipe Hunting", "Discover all cooking recipes", locations[0].location_id, None),
            ("Card Collector", "Catch all enemy cards", locations[0].location_id, None),
            ("Merlee's Fortune", "Get fortune readings from Merlee", locations[7].location_id, None),
        ]
        
        quests = []
        for name, desc, start_loc, reward_item in quests_data:
            quests.append(SideQuest(name=name, description=desc, start_location_id=start_loc, reward_item_id=reward_item))
        db.add_all(quests)
        db.commit()
        print(f"  ✅ Created {len(quests)} side quests\n")
        
        # ===== BLOCKS =====
        print("📦 Creating Blocks...")
        blocks = []
        # Add some blocks with items in various locations
        for i, location in enumerate(locations[:10]):  # First 10 locations
            if i % 3 == 0:  # Every third location gets a breakable block with Mushroom
                blocks.append(BlockContainer(
                    location_id=location.location_id,
                    block_type=BlockType.breakable,
                    contains_item_id=items[0].item_id
                ))
            elif i % 3 == 1:  # Star blocks
                blocks.append(BlockContainer(
                    location_id=location.location_id,
                    block_type=BlockType.star,
                    contains_item_id=None
                ))
            else:  # Movable blocks
                blocks.append(BlockContainer(
                    location_id=location.location_id,
                    block_type=BlockType.movable,
                    contains_item_id=None
                ))
        
        db.add_all(blocks)
        db.commit()
        print(f"  ✅ Created {len(blocks)} blocks\n")
        
        # ===== OBJECTS =====
        print("🎯 Creating Objects...")
        objects_data = [
            # Yold Town & Lineland
            ("Arrow Sign", "arrow", "Points to Yold Desert", locations[0].location_id),
            ("Warp Pipe", "warp", "Green pipe to underground area", locations[1].location_id),
            ("Treasure Chest", "chest", "Contains a Pixl", locations[1].location_id),
            ("Ladder", "ladder", "Climbs to higher platform", locations[2].location_id),
            
            # Gloam Valley
            ("Lift Platform", "elevator", "Moves between floors", locations[7].location_id),
            ("Jump Platform", "trampoline", "Bounces player upward", locations[8].location_id),
            ("Heart Pillar", "pillar", "Accepts Pure Heart", locations[9].location_id),
            
            # The Bitlands
            ("Spinning Device", "spinner", "Rotates platforms", locations[10].location_id),
            ("Flip Block", "flip_block", "Reveals hidden path in 3D", locations[10].location_id),
            ("Treasure Chest", "chest", "Contains Barry", locations[12].location_id),
            
            # Outer Space
            ("Space Gate", "portal", "Transport between planets", locations[13].location_id),
            ("Squarp Hole", "warp", "Dimensional warp point", locations[13].location_id),
            ("Geyser", "geyser", "Shoots player upward", locations[15].location_id),
            
            # Floro Caverns
            ("Minecart", "vehicle", "Rides on rails", locations[16].location_id),
            ("Stone Tablet", "tablet", "Elemental puzzle piece", locations[17].location_id),
            ("Orb Pedestal", "pedestal", "Holds colored orb", locations[17].location_id),
            
            # Sammer Kingdom
            ("Battle Arena", "arena", "Duel platform", locations[20].location_id),
            
            # Underwhere/Overthere
            ("Boat", "vehicle", "Travels River Twygz", locations[21].location_id),
            ("Cloud Platform", "platform", "Floating cloud", locations[23].location_id),
            ("Red Apple Tree", "tree", "Produces Red Apples", locations[24].location_id),
            
            # Flipside/Flopside
            ("Heart Pillar", "pillar", "Flipside tower pillar", locations[25].location_id),
            ("Treasure Chest", "chest", "Contains rare item", locations[25].location_id),
            ("Grab Block", "throw_block", "Throwable block", locations[26].location_id),
            ("Coin Block", "coin_block", "Generates coins when hit", locations[26].location_id),
        ]
        
        objects = []
        for name, obj_type, props, loc_id in objects_data:
            objects.append(Object(name=name, object_type=obj_type, properties=props, location_id=loc_id))
        db.add_all(objects)
        db.commit()
        print(f"  ✅ Created {len(objects)} objects\n")
        
        # ===== NAVIGATION OBJECTS =====
        print("🚪 Creating Navigation Objects...")
        nav_objects_data = [
            # Doors throughout the game
            (NavigationType.door, "Entrance to Yold Ruins", locations[1].location_id),
            (NavigationType.door, "Exit from Yold Desert", locations[2].location_id),
            (NavigationType.door, "Merlee's Mansion entrance", locations[7].location_id),
            (NavigationType.door, "Dotwood Tree entrance", locations[8].location_id),
            (NavigationType.door, "Fort Francis main door", locations[11].location_id),
            (NavigationType.door, "Whoa Zone portal", locations[15].location_id),
            (NavigationType.door, "Floro Caverns gate", locations[16].location_id),
            (NavigationType.door, "Underwhere entrance", locations[21].location_id),
            (NavigationType.door, "Castle Bleck gate", locations[28].location_id),
            
            # Elevators
            (NavigationType.elevator, "Merlee's Mansion lift", locations[7].location_id),
            (NavigationType.elevator, "Fort Francis elevator", locations[11].location_id),
            (NavigationType.elevator, "Castle Bleck lift", locations[28].location_id),
            
            # Save Blocks
            (NavigationType.save_block, "Flipside save point", locations[25].location_id),
            (NavigationType.save_block, "Flopside save point", locations[26].location_id),
            (NavigationType.save_block, "Yold Town save", locations[0].location_id),
            (NavigationType.save_block, "Gloam Valley save", locations[7].location_id),
            (NavigationType.save_block, "Downtown of Crag save", locations[16].location_id),
            
            # Star Blocks
            (NavigationType.star_block, "Flipside star checkpoint", locations[25].location_id),
            (NavigationType.star_block, "Flopside star checkpoint", locations[26].location_id),
            
            # Dimensional Rifts
            (NavigationType.rift, "Hidden rift to bonus area", locations[10].location_id),
            (NavigationType.rift, "Secret dimensional door", locations[31].location_id),
            
            # Arrow signs
            (NavigationType.arrow, "Points to next area", locations[0].location_id),
            (NavigationType.arrow, "Directional marker", locations[13].location_id),
        ]
        
        nav_objects = []
        for nav_type, props, loc_id in nav_objects_data:
            nav_objects.append(NavigationObject(type=nav_type, properties=props, location_id=loc_id))
        db.add_all(nav_objects)
        db.commit()
        print(f"  ✅ Created {len(nav_objects)} navigation objects\n")
        
        # ===== OBSTACLES =====
        print("⚠️ Creating Obstacles...")
        obstacles_data = [
            # Bottomless pits
            ("Bottomless Pit", "Instant KO if fallen into", locations[1].location_id),
            ("Bottomless Pit", "Deep chasm", locations[2].location_id),
            ("Bottomless Pit", "Endless void", locations[14].location_id),
            ("Bottomless Pit", "Space void", locations[15].location_id),
            
            # Spike hazards
            ("Spike Trap", "Floor spikes that rise periodically", locations[8].location_id),
            ("Spike Trap", "Wall spikes", locations[11].location_id),
            ("Spike Ceiling", "Descending spike ceiling", locations[7].location_id),
            ("Spike Trap", "Underwhere spikes", locations[21].location_id),
            
            # Fire hazards
            ("Fire Bar", "Rotating fire obstacle", locations[1].location_id),
            ("Fire Bar", "Castle Bleck fire bars", locations[28].location_id),
            ("Fire-spitting Lamp", "Shoots fireballs", locations[7].location_id),
            ("Fire-spitting Lamp", "Candle hazard", locations[17].location_id),
            
            # Electrical barriers
            ("Electrical Barrier", "Electric rail obstacle", locations[7].location_id),
            
            # Environmental hazards
            ("Quicksand", "Slowly sinks the player", locations[2].location_id),
            ("Dark Area", "Requires fire to illuminate", locations[21].location_id),
            ("Hedron", "Floating geometric obstacle", locations[15].location_id),
            
            # Enemy-like obstacles
            ("Gnip", "Stone face obstacle", locations[7].location_id),
            ("Gnaw", "Moving jaw trap", locations[7].location_id),
            ("Floro Sprout", "Mind-control plant", locations[17].location_id),
            
            # Locked doors
            ("Locked Door", "Requires key to open", locations[25].location_id),
            ("Locked Door", "Key door in ruins", locations[1].location_id),
            ("Locked Door", "Fort Francis security", locations[11].location_id),
            ("Yellow Block", "Requires Cudge to break", locations[17].location_id),
        ]
        
        obstacles = []
        for obs_type, behavior, loc_id in obstacles_data:
            obstacles.append(Obstacle(type=obs_type, behavior=behavior, location_id=loc_id))
        db.add_all(obstacles)
        db.commit()
        print(f"  ✅ Created {len(obstacles)} obstacles\n")
        
        # ===== SWITCHES =====
        print("🔘 Creating Switches...")
        switches_data = [
            # Switches that control doors
            ("! Switch", locations[7].location_id, nav_objects[2].navobj_id),  # Controls Merlee's door
            ("! Switch", locations[28].location_id, nav_objects[8].navobj_id),  # Controls Castle Bleck gate
            
            # Switches that control elevators
            ("Lever", locations[7].location_id, nav_objects[9].navobj_id),  # Controls Merlee's lift
            ("Lever", locations[11].location_id, nav_objects[10].navobj_id),  # Controls Fort Francis elevator
            
            # Gravity switches (no specific target, changes environment)
            ("Gravity Switch", locations[7].location_id, None),
            ("Gravity Switch", locations[11].location_id, None),
            
            # Additional switches
            ("! Switch", locations[17].location_id, nav_objects[6].navobj_id),  # Controls Floro gate
            ("Lever", locations[21].location_id, None),  # Underwhere puzzle
            ("! Switch", locations[10].location_id, nav_objects[19].navobj_id),  # Controls rift
        ]
        
        switches = []
        for switch_type, loc_id, target_navobj in switches_data:
            switches.append(Switch(switch_type=switch_type, location_id=loc_id, target_navobj_id=target_navobj))
        db.add_all(switches)
        db.commit()
        print(f"  ✅ Created {len(switches)} switches\n")
        
        db.commit()
        print("=" * 60)
        print("✨ DATABASE SEEDED SUCCESSFULLY! ✨")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"  • {db.query(Chapter).count()} Chapters")
        print(f"  • {db.query(Character).count()} Characters")
        print(f"  • {db.query(PlayableCharacter).count()} Playable Characters")
        print(f"  • {db.query(Pixl).count()} Pixls")
        print(f"  • {db.query(Enemy).count()} Enemies")
        print(f"  • {db.query(Boss).count()} Bosses")
        print(f"  • {db.query(Item).count()} Items")
        print(f"  • {db.query(Location).count()} Locations")
        print(f"  • {db.query(StatusEffect).count()} Status Effects")
        print(f"  • {db.query(SideQuest).count()} Side Quests")
        print(f"  • {db.query(BlockContainer).count()} Blocks")
        print(f"  • {db.query(Object).count()} Objects")
        print(f"  • {db.query(NavigationObject).count()} Navigation Objects")
        print(f"  • {db.query(Obstacle).count()} Obstacles")
        print(f"  • {db.query(Switch).count()} Switches")
        print("\n🎮 Ready to explore the world of Super Paper Mario!")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" SUPER PAPER MARIO - COMPREHENSIVE DATABASE SEED")
    print("=" * 60 + "\n")
    seed_comprehensive()
    print("\n" + "=" * 60)
