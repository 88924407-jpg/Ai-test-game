# data.py

ITEM_ENCYCLOPEDIA = {
    "Dirt": {
        "rarity": "Common", "category": "material", "icon": "🟤",
        "description": "Basic earthy dirt collected from cave floors.",
        "use": "Used as a basic building block for crafting Compound Dirt.",
        "color": "#E5D4C0"
    },
    "Worms": {
        "rarity": "Common", "category": "material", "icon": "🐛",
        "description": "Squirmy little underground critters.",
        "use": "Bait used alongside Dirt to compound rich terrain.",
        "color": "#D1C2A5"
    },
    "Roots": {
        "rarity": "Common", "category": "material", "icon": "🌿",
        "description": "Fibrous and tough plant fibers.",
        "use": "Used as binding material to tie tools like the Pebble Axe together.",
        "color": "#C8E6C9"
    },
    "Pebbles": {
        "rarity": "Common", "category": "material", "icon": "🪨",
        "description": "Hard stone fragments found while digging.",
        "use": "Used for heavy construction and blunt tools.",
        "color": "#CFD8DC"
    },
    "Coal": {
        "rarity": "Common", "category": "material", "icon": "⬛",
        "description": "Dark combustible rock found deep in the cave.",
        "use": "Fuel used with the Stone Oven to smelt metal ores.",
        "color": "#B0BEC5"
    },
    "Soil": {
        "rarity": "Uncommon", "category": "material", "icon": "🪴",
        "description": "Nutrient-rich dark earth.",
        "use": "Accumulate 5 to craft Fine dirt.",
        "color": "#D7CCC8"
    },
    "Old Carrots": {
        "rarity": "Uncommon", "category": "food", "icon": "🥕",
        "description": "Shriveled and old cave roots.",
        "use": "Can be snacked on or traded later.",
        "color": "#FFE0B2"
    },
    "Dead Flower": {
        "rarity": "Uncommon", "category": "material", "icon": "🥀",
        "description": "Faded flora with botanical potential.",
        "use": "Can be studied or used in crafting recipes.",
        "color": "#E1BEE7"
    },
    "Fresh Carrots": {
        "rarity": "Rare", "category": "food", "icon": "🥕",
        "description": "Crisp and delicious cave harvest.",
        "use": "Provides high nourishment and trade value.",
        "color": "#FFCCBC"
    },
    "Roses": {
        "rarity": "Rare", "category": "material", "icon": "🌹",
        "description": "Fragrant and beautiful rare flora.",
        "use": "Admire its beauty or trade for rare goods.",
        "color": "#FFCDD2"
    },
    "Perfect Soil": {
        "rarity": "Rare", "category": "material", "icon": "✨",
        "description": "Pristine, glowing earth.",
        "use": "Instantly fulfills Fine dirt recipe requirements and unlocks the crafting tree!",
        "color": "#FFF9C4"
    },
    "Metal Fragments": {
        "rarity": "Rare", "category": "material", "icon": "🔩",
        "description": "Raw metallic chunks extracted from cave walls.",
        "use": "Smelted using Coal and the Stone Oven to produce Molten Metal.",
        "color": "#B3E5FC"
    },
    "Compound Dirt": {
        "rarity": "Crafted", "category": "crafted", "icon": "🧱",
        "description": "An upgraded composite soil block.",
        "use": "Used for sturdy underground foundations.",
        "color": "#D7CCC8"
    },
    "Fine dirt": {
        "rarity": "Crafted", "category": "crafted", "icon": "🟫",
        "description": "Ultra-smooth silt.",
        "use": "Primary foundation for building high-tier stone structures like the Stone Oven.",
        "color": "#BCAAA4"
    },
    "Molten Metal": {
        "rarity": "Rare", "category": "crafted", "icon": "♨️",
        "description": "Superheated glowing liquid metal.",
        "use": "Advanced crafting material for high-tier forged items.",
        "color": "#FFAB91"
    },
    "Pebble Axe": {
        "rarity": "Crafted", "category": "tool", "icon": "🪓",
        "description": "A crude stone axe tied with roots.",
        "use": "Passive Tool: Permanently multiplies materials harvested when digging!",
        "color": "#D7CCC8"
    },
    "Stone Oven": {
        "rarity": "Crafted", "category": "tool", "icon": "🔥",
        "description": "A hearth built from fine dirt and pebbles.",
        "use": "Culinary Station: Unlocks heat processing and advanced metal smelting.",
        "color": "#FFCC80"
    }
}

def _catalog_items(category, color, entries):
    return {
        name: {
            "rarity": rarity,
            "category": category,
            "icon": icon,
            "description": description,
            "use": use,
            "color": color,
        }
        for name, icon, rarity, description, use in entries
    }


ITEM_ENCYCLOPEDIA.update({
    **_catalog_items("food", "#F8E8C8", [
        ("Cave Mushrooms", "🍄", "Common", "Pale mushrooms growing in damp cave alcoves.", "A simple meal or ingredient for hearty cave cooking."),
        ("Roasted Cave Mushrooms", "🍄", "Uncommon", "Crisp mushrooms roasted over a small fire.", "A filling snack for a long expedition."),
        ("Wild Berries", "🫐", "Common", "A handful of tart berries gathered from the cavern edge.", "Eat fresh or save for a trail ration."),
        ("River Trout", "🐟", "Uncommon", "A fresh trout pulled from an underground stream.", "Cook it for a nourishing meal."),
        ("Smoked Trout", "🐟", "Crafted", "A trout preserved with fragrant wood smoke.", "A long-lasting food for journeys."),
        ("Roast Boar", "🍖", "Uncommon", "Savory boar meat cooked over an open flame.", "A substantial meal after a successful hunt."),
        ("Jerky Strips", "🥩", "Crafted", "Thin strips of meat dried for travel.", "Compact trail food that keeps well."),
        ("Honeycomb", "🍯", "Rare", "A golden piece of honeycomb from a hidden nest.", "A sweet treat and useful cooking ingredient."),
        ("Caveberry Tart", "🥧", "Crafted", "A rustic tart filled with sweet caveberries.", "A special meal made from gathered fruit."),
        ("Herb Stew", "🍲", "Crafted", "A warming stew of roots and wild herbs.", "Restores spirits during a chilly cave trek."),
        ("Root Vegetable Soup", "🥣", "Uncommon", "A simple soup made from freshly dug vegetables.", "A wholesome meal made from the harvest."),
        ("Dried Fruit Mix", "🥜", "Crafted", "Berries and fruit dried into a lightweight mix.", "Convenient food to carry while exploring."),
    ]),
    **_catalog_items("weapon", "#E8D9D0", [
        ("Flint Spear", "🗡️", "Common", "A sturdy wooden spear tipped with chipped flint.", "A reliable first weapon for hunting and defense."),
        ("Bone Club", "🏏", "Common", "A heavy branch reinforced with polished bone.", "A simple blunt weapon for close encounters."),
        ("Stone Knife", "🔪", "Common", "A sharp flaked-stone blade bound to a short grip.", "Useful for cutting, carving, and close defense."),
        ("Flint Hatchet", "🪓", "Uncommon", "A balanced hatchet with a carefully knapped flint head.", "A versatile tool and dependable weapon."),
        ("Bone Dagger", "🗡️", "Uncommon", "A slim dagger carved from dense animal bone.", "Lightweight protection for quick-moving hunters."),
        ("Obsidian Blade", "⚔️", "Rare", "A dark glassy blade with a keen, gleaming edge.", "A prized weapon that needs careful handling."),
        ("Stone Mace", "🔨", "Uncommon", "A rounded stone head secured to a hardwood handle.", "A powerful blunt weapon for sturdy hands."),
        ("Hunting Bow", "🏹", "Uncommon", "A flexible wooden bow strung with braided fiber.", "Lets a hunter take aim from a safer distance."),
        ("Reinforced Bow", "🏹", "Rare", "A hunting bow strengthened with sinew bindings.", "A stronger bow for experienced marksmen."),
        ("Sling", "🪨", "Common", "A woven sling made to launch small stones.", "A light ranged weapon with easy-to-find ammunition."),
        ("Bone Harpoon", "🔱", "Uncommon", "A barbed bone point fixed to a long shaft.", "Designed for large fish and dangerous game."),
        ("War Club", "🪵", "Uncommon", "A dense hardwood club carved for a firm grip.", "A durable weapon for defending the settlement."),
    ]),
    **_catalog_items("fishing", "#DCEBF0", [
        ("Fishing Rod", "🎣", "Common", "A flexible branch fitted with a simple line.", "Your basic tool for fishing in underground waters."),
        ("Reed Fishing Rod", "🎣", "Uncommon", "A light rod fashioned from strong river reeds.", "A nimble rod for calmer streams."),
        ("Bone Hook", "🪝", "Common", "A small hook carved from a hard sliver of bone.", "A reusable hook for catching cave fish."),
        ("Stone Hook", "🪝", "Uncommon", "A carefully chipped stone hook with a sharp point.", "A tough hook for larger catches."),
        ("Braided Fishing Line", "🧵", "Common", "Plant fibers twisted into a sturdy fishing line.", "Connects your rod to a hook or lure."),
        ("Woven Fishing Net", "🕸️", "Uncommon", "A broad net woven from strong plant fibers.", "Useful for gathering small fish in shallow water."),
        ("Bait Bundle", "🪱", "Common", "Worms and grubs bundled together for bait.", "Attracts hungry fish to your line."),
        ("Grub Bait", "🐛", "Common", "Soft grubs collected from rich cave soil.", "Simple bait for an underground fishing trip."),
        ("Feather Lure", "🪶", "Uncommon", "A bright feather lure tied to a tiny stone hook.", "Draws curious fish toward the surface."),
        ("River Float", "🪵", "Common", "A carved piece of light wood that keeps a line afloat.", "Helps spot a tug beneath the water."),
        ("Fish Basket", "🧺", "Uncommon", "A ventilated basket woven from reeds.", "Carries a fresh catch back to camp."),
        ("Fishing Spear", "🔱", "Uncommon", "A straight spear with a narrow, barbed tip.", "For catching fish in clear, shallow pools."),
    ]),
    **_catalog_items("farming", "#E3EBD9", [
        ("Stone Hoe", "🪓", "Common", "A broad stone blade lashed to a sturdy handle.", "Breaks and turns packed soil for planting."),
        ("Bone Hoe", "🌿", "Uncommon", "A light, curved farming tool carved from bone.", "Prepares small plots with careful strokes."),
        ("Seed Pouch", "👝", "Common", "A small leather pouch for keeping seeds dry.", "Stores seeds between planting seasons."),
        ("Wild Grain Seeds", "🌾", "Common", "Hardy seeds gathered from cave-side grasses.", "Can be planted to grow a useful grain crop."),
        ("Cave Carrot Seeds", "🥕", "Common", "Tiny seeds saved from a bright cave carrot.", "Plant in prepared soil for a root harvest."),
        ("Berry Seeds", "🫐", "Uncommon", "Seeds gathered from a cluster of ripe wild berries.", "Grow berry bushes near the settlement."),
        ("Plant Fiber", "🧶", "Common", "Long fibers stripped from tough cave plants.", "Useful for weaving, tying, and garden repairs."),
        ("Compost", "🪱", "Common", "Rich compost made from leaves and food scraps.", "Adds nutrients to tired garden soil."),
        ("Irrigation Jug", "🏺", "Uncommon", "A clay jug with a narrow spout for careful watering.", "Carries water to seedlings without flooding them."),
        ("Woven Scarecrow", "🪹", "Uncommon", "A simple figure woven from stalks and old cloth.", "Keeps curious cave birds away from crops."),
        ("Harvest Basket", "🧺", "Common", "A roomy basket woven for gathering vegetables.", "Carries crops from the garden to camp."),
        ("Enriched Soil", "🪴", "Crafted", "Dark garden soil mixed with compost and leaf mold.", "A fertile base for healthy crops."),
    ]),
    **_catalog_items("hunting", "#E9E1D8", [
        ("Tracking Kit", "🐾", "Uncommon", "A bundle of charcoal, cord, and trail markers.", "Helps record tracks and follow animal trails."),
        ("Bone Trap", "🪤", "Uncommon", "A small spring trap assembled from bone and cord.", "Catches small game along a well-used trail."),
        ("Snare Trap", "🪢", "Common", "A loop of braided fiber set along an animal path.", "A basic trap for small cave-dwelling game."),
        ("Animal Bait", "🥩", "Common", "A fragrant bundle prepared to attract wild game.", "Lures animals toward a chosen hunting spot."),
        ("Hide Scraper", "🪒", "Common", "A flat stone scraper with a comfortable bone grip.", "Cleans and prepares hides for useful materials."),
        ("Fur Pelt", "🐾", "Uncommon", "A warm pelt gathered from a successful hunt.", "Can be used for clothing or shelter insulation."),
        ("Deer Antler", "🦌", "Uncommon", "A branching antler shed in the forest tunnels.", "Useful for handles, hooks, and carved tools."),
        ("Boar Hide", "🐗", "Uncommon", "A thick hide from a cave boar.", "A durable material for armor and sturdy packs."),
        ("Wolf Fang", "🦷", "Rare", "A long fang found near a wolf's den.", "A rare crafting piece and keepsake of a difficult hunt."),
        ("Camouflage Wrap", "🍂", "Uncommon", "A leafy wrap that breaks up a hunter's outline.", "Helps a hunter blend into the cave-side brush."),
        ("Sinew Cord", "🪢", "Common", "Strong animal sinew dried and twisted into cord.", "Binds tools and makes dependable bowstrings."),
        ("Trophy Rack", "🪵", "Crafted", "A carved wooden rack for displaying hunting trophies.", "Decorates a settlement with memorable keepsakes."),
    ]),
})

CRAFT_TREE_PAPERS = {
    "Farming": {
        "name": "Field Sketch",
        "description": "A folded page with planting rows and a tiny sprout drawing.",
    },
    "Fishing": {
        "name": "River Sketch",
        "description": "A hand-drawn stream map marks promising fishing pools.",
    },
    "Hunting": {
        "name": "Trail Sketch",
        "description": "A charcoal drawing shows tracks leading through the cave.",
    },
}

for paper in CRAFT_TREE_PAPERS.values():
    ITEM_ENCYCLOPEDIA[paper["name"]] = {
        "rarity": "Rare",
        "category": "research",
        "icon": "📜",
        "description": paper["description"],
        "use": "Reveals a new illustrated crafting section.",
        "color": "#F1E5CF",
    }

CRAFT_TREE_BRANCHES = {
    "Farming": {
        "icon": "🌱",
        "action": "Farm",
        "paper": CRAFT_TREE_PAPERS["Farming"]["name"],
        "color": "#E3EBD9",
        "starter_recipe": {"Roots": 2, "Pebbles": 2, "Dirt": 2},
        "rewards": [
            "Wild Grain Seeds", "Cave Carrot Seeds", "Berry Seeds",
            "Plant Fiber", "Compost", "Enriched Soil", "Soil",
        ],
        "tools": [
            ("Garden Trowel", "🪴", "Turns a small patch of cave soil for planting."),
            ("Digging Fork", "🍴", "Loosens dense earth and brings up extra seed finds."),
            ("Hand Plow", "🚜", "Opens a longer furrow for dependable harvests."),
            ("Seed Drill", "🌾", "Plants gathered seeds evenly and improves crop yields."),
            ("Irrigation Spade", "💧", "Channels water toward useful roots and seed crops."),
            ("Pruning Shears", "✂️", "Collects plant fiber and berry seeds without waste."),
            ("Harvest Sickle", "🌾", "Gathers mature grain and cave vegetables efficiently."),
            ("Field Rake", "🪵", "Finds compost and prepares rich ground for planting."),
            ("Terrace Plow", "⛰️", "Works steep cave plots and turns up enriched soil."),
            ("Master Cultivator", "🌿", "A complete farming kit for the largest, richest harvests."),
        ],
        "upgrades": [
            ("Seed Selection", "🌱", "Sorts the strongest seeds to improve each harvest."),
            ("Rich Compost Blend", "🪱", "Feeds crops with nutrients for larger yields."),
            ("Drip Irrigation Kit", "🏺", "Delivers water steadily, improving seed and soil finds."),
            ("Crop Rotation Plan", "📋", "Keeps plots fertile and produces more varied crops."),
            ("Raised Bed Frames", "🪚", "Protects cave crops and boosts the amount gathered."),
            ("Greenhouse Canopy", "⛺", "Traps warmth and supports a broader range of plants."),
            ("Pollinator Garden", "🌼", "Attracts cave insects that help crops and berries thrive."),
            ("Waterwheel Pump", "⚙️", "Moves stream water to the fields for more reliable harvests."),
            ("Terrace Retaining Wall", "🧱", "Holds rich soil in place on steep planting terraces."),
            ("Bountiful Harvest Charm", "✨", "A farmer's keepsake that maximizes every gathering trip."),
        ],
    },
    "Fishing": {
        "icon": "🎣",
        "action": "Fish",
        "paper": CRAFT_TREE_PAPERS["Fishing"]["name"],
        "color": "#DCEBF0",
        "starter_recipe": {"Roots": 2, "Pebbles": 1, "Worms": 2},
        "rewards": [
            "River Trout", "Worms", "Bait Bundle", "Grub Bait",
            "Feather Lure", "River Float", "Wild Berries",
        ],
        "tools": [
            ("Driftwood Rod", "🎣", "Casts a simple line into calm underground pools."),
            ("River Net", "🕸️", "Sweeps shallow water for fish and usable bait."),
            ("Bone Gaff", "🔱", "Lifts heavier catches from fast-moving streams."),
            ("Spinner Lure", "🪝", "Draws curious fish from a wider stretch of water."),
            ("Split-Reed Trap", "🧺", "Leaves a passive trap in narrow cave channels."),
            ("Deepwater Pole", "🎣", "Reaches pools where larger trout gather."),
            ("Barbed Handline", "🧵", "Holds firm against strong fish and deep currents."),
            ("Current Skiff", "🛶", "Reaches remote pools with better bait and catches."),
            ("Echo Float", "🪵", "Signals fish activity and helps find rare fishing supplies."),
            ("Master Angling Rig", "🐟", "A complete rig for the richest underground fishing trips."),
        ],
        "upgrades": [
            ("Braided Line Upgrade", "🧶", "A stronger line that brings in more fish per trip."),
            ("Barbed Hook Set", "🪝", "Keeps catches secure and improves bait recovery."),
            ("Scented Bait Mix", "🪱", "Attracts more fish and expands the possible catch."),
            ("Weighted Float", "⚓", "Keeps the line steady in deeper, faster water."),
            ("Net Reinforcement", "🕸️", "Strengthens the mesh to hold a larger catch."),
            ("Tidal Almanac", "📖", "Tracks stream patterns to locate productive pools."),
            ("Smokehouse Rack", "🔥", "Preserves surplus fish and improves each expedition's haul."),
            ("Stream Channel Markers", "🪨", "Marks safe fishing spots and productive currents."),
            ("Fish Finder Chime", "🔔", "Uses water echoes to locate schools of cave fish."),
            ("Bountiful Catch Charm", "✨", "A fisher's keepsake that maximizes every trip to the water."),
        ],
    },
    "Hunting": {
        "icon": "🏹",
        "action": "Hunt",
        "paper": CRAFT_TREE_PAPERS["Hunting"]["name"],
        "color": "#E9E1D8",
        "starter_recipe": {"Roots": 3, "Pebbles": 2, "Coal": 1},
        "rewards": [
            "Deer Antler", "Sinew Cord", "Animal Bait", "Fur Pelt",
            "Boar Hide", "Wolf Fang", "Old Carrots",
        ],
        "tools": [
            ("Tracking Staff", "🐾", "Reads animal trails to find useful hunting materials."),
            ("Flint Sling", "🪨", "A quiet ranged weapon for small-game hunts."),
            ("Bone Knife", "🔪", "Prepares hides and sinew from a successful hunt."),
            ("Scent Trail Kit", "🌿", "Follows game trails to find bait and animal tracks."),
            ("Spring Snare", "🪤", "Catches small game while you scout the cave."),
            ("Longbow", "🏹", "A reliable bow for reaching larger game from a distance."),
            ("Hide Scraper Kit", "🪒", "Salvages more pelts and hides from each expedition."),
            ("Antler Spear", "🔱", "A sturdy weapon for tracking and hunting tougher prey."),
            ("Camouflage Cloak", "🍂", "Conceals your approach and improves rare material finds."),
            ("Master Tracker's Kit", "🎯", "A complete hunting kit for the most rewarding expeditions."),
        ],
        "upgrades": [
            ("Quiet Footwraps", "👣", "Muffles your steps so more game stays within reach."),
            ("Sharpened Flint Set", "🪨", "Keeps hunting tools keen and improves recovered materials."),
            ("Sinew Bowstring", "🪢", "Strengthens a bow for more successful hunts."),
            ("Scent Mask", "🍃", "Hides your trail and helps locate wary animals."),
            ("Reinforced Snare", "🪤", "Improves trap catches and the supplies recovered."),
            ("Fletched Arrow Bundle", "🏹", "Provides dependable arrows for longer hunting trips."),
            ("Wind Reading Kit", "🌬️", "Helps approach game from downwind and find better trails."),
            ("Pelt Curing Rack", "🪵", "Preserves hides and increases useful hunting materials."),
            ("Trophy Lure", "🦌", "Attracts larger game and improves rare finds."),
            ("Hunter's Focus Charm", "✨", "A hunter's keepsake that maximizes every expedition."),
        ],
    },
}

CRAFT_TREE_ITEMS = {}
CRAFT_TREE_RECIPES = {}

for branch, branch_data in CRAFT_TREE_BRANCHES.items():
    for track in ("tools", "upgrades"):
        previous_item = None
        for tier, (item_name, icon, description) in enumerate(branch_data[track], start=1):
            rarity = "Common" if tier <= 3 else "Uncommon" if tier <= 6 else "Rare" if tier <= 8 else "Crafted"
            is_tool = track == "tools"
            track_label = "tool" if is_tool else "upgrade"
            ITEM_ENCYCLOPEDIA[item_name] = {
                "rarity": rarity,
                "category": "tool" if is_tool else "crafted",
                "icon": icon,
                "description": description,
                "use": (
                    f"Tier {tier} {branch.lower()} {track_label}: contributes +{tier} to "
                    "gathering yield and unlocks more resource finds."
                ),
                "color": branch_data["color"],
            }
            CRAFT_TREE_ITEMS[item_name] = {
                "branch": branch,
                "track": track,
                "tier": tier,
            }

            if is_tool and tier == 1:
                ingredients = dict(branch_data["starter_recipe"])
            else:
                resource = branch_data["rewards"][(tier - 1) % len(branch_data["rewards"])]
                cost = 1 + (tier - 1) // (3 if is_tool else 2)
                ingredients = {resource: cost}
                if previous_item:
                    ingredients[previous_item] = 1

            CRAFT_TREE_RECIPES[item_name] = ingredients
            previous_item = item_name


DEFAULT_RECIPES = {
    "Compound Dirt": {"Dirt": 3, "Worms": 2},
    "Fine dirt": {"alternatives": [{"Soil": 5}, {"Perfect Soil": 1}]},
    "Pebble Axe": {"Pebbles": 4, "Roots": 3},
    "Stone Oven": {"Fine dirt": 2, "Pebbles": 10},
    "Molten Metal": {"Metal Fragments": 3, "Coal": 2}
}

DEFAULT_RECIPES.update(CRAFT_TREE_RECIPES)
