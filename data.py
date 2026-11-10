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

DEFAULT_RECIPES = {
    "Compound Dirt": {"Dirt": 3, "Worms": 2},
    "Fine dirt": {"alternatives": [{"Soil": 5}, {"Perfect Soil": 1}]},
    "Pebble Axe": {"Pebbles": 4, "Roots": 3},
    "Stone Oven": {"Fine dirt": 2, "Pebbles": 10},
    "Molten Metal": {"Metal Fragments": 3, "Coal": 2}
}