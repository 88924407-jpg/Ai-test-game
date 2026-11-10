import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Caveman Tycoon",
    page_icon="🦴",
    layout="wide"
)

# Custom CSS for earthy theme, styling, and 'q' key listener injection
st.markdown("""
<style>
    .stApp {
        background-color: #F5EBDC;
        color: #32281E;
    }
    h1, h2, h3 {
        color: #78552D !important;
        font-family: Arial, sans-serif;
    }
    /* Style the native sidebar to be pastel blue */
    [data-testid="stSidebar"] {
        background-color: #E3EEF8;
        border-right: 2px solid #A2C4E0;
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #1A365D !important;
    }
    .stButton>button {
        background-color: #78552D;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #B46E32;
        color: white;
    }
    .item-shadow {
        color: rgba(0, 0, 0, 0.25);
        text-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
        filter: blur(1.5px);
        user-select: none;
    }
    .craft-node {
        background-color: #EEDCC5;
        border: 2px solid #B46E32;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
</style>

<!-- JavaScript Hotkey Listener: Press 'q' to open Admin Panel -->
<script>
    document.addEventListener('keydown', function(event) {
        // Only trigger if not typing inside an input or textarea
        if (event.key.toLowerCase() === 'q' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            event.preventDefault();
            // Trigger streamlit rerun by navigating with query param
            const url = new URL(window.location.href);
            url.searchParams.set('admin_mode', 'true');
            window.location.href = url.toString();
        }
    });
</script>
""", unsafe_allow_html=True)

# Initialize Session State variables
if "state" not in st.session_state:
    st.session_state.state = "MENU"

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Dirt": 0, "Worms": 0, "Roots": 0, "Pebbles": 0,
        "Soil": 0, "Old Carrots": 0, "Dead Flower": 0,
        "Fresh Carrots": 0, "Roses": 0, "Perfect Soil": 0,
        "Compound Dirt": 0, "Fine dirt": 0, 
        "Pebble Axe": 0, "Stone Oven": 0
    }

if "recipes" not in st.session_state:
    st.session_state.recipes = {
        "Compound Dirt": {"Dirt": 3, "Worms": 2},
        "Fine dirt": {"alternatives": [{"Soil": 5}, {"Perfect Soil": 1}]},
        "Pebble Axe": {"Pebbles": 4, "Roots": 3},
        "Stone Oven": {"Fine dirt": 2, "Pebbles": 10}
    }

if "tool_boosters" not in st.session_state:
    st.session_state.tool_boosters = {
        "Pebble Axe": {"level": 1, "multiplier": 2},
        "Stone Oven": {"level": 1, "multiplier": 1}
    }

if "show_inventory_modal" not in st.session_state:
    st.session_state.show_inventory_modal = False

if "inv_tab" not in st.session_state:
    st.session_state.inv_tab = "all"

if "inv_sort_by" not in st.session_state:
    st.session_state.inv_sort_by = "Rarity"

if "inv_sort_order" not in st.session_state:
    st.session_state.inv_sort_order = "Standard (Ascending)"

if "message" not in st.session_state:
    st.session_state.message = ""

if "message_expiry" not in st.session_state:
    st.session_state.message_expiry = 0.0

if "show_actions" not in st.session_state:
    st.session_state.show_actions = False

if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

# Enhanced item registry with icons, descriptions, and uses
ITEM_ENCYCLOPEDIA = {
    "Dirt": {
        "rarity": "Common", "category": "material", "icon": "🟤",
        "description": "Basic earthy dirt collected from cave floors.",
        "use": "Used as a basic building block for crafting Compound Dirt."
    },
    "Worms": {
        "rarity": "Common", "category": "material", "icon": "🐛",
        "description": "Squirmy little underground critters.",
        "use": "Bait used alongside Dirt to compound rich terrain."
    },
    "Roots": {
        "rarity": "Common", "category": "material", "icon": "🌿",
        "description": "Fibrous and tough plant fibers.",
        "use": "Used as binding material to tie tools like the Pebble Axe together."
    },
    "Pebbles": {
        "rarity": "Common", "category": "material", "icon": "🪨",
        "description": "Hard stone fragments found while digging.",
        "use": "Used for heavy construction and blunt tools."
    },
    "Soil": {
        "rarity": "Uncommon", "category": "material", "icon": "🪴",
        "description": "Nutrient-rich dark earth.",
        "use": "Accumulate 5 to craft Fine dirt."
    },
    "Old Carrots": {
        "rarity": "Uncommon", "category": "food", "icon": "🥕",
        "description": "Shriveled and old cave roots.",
        "use": "Can be snacked on or traded later."
    },
    "Dead Flower": {
        "rarity": "Uncommon", "category": "material", "icon": "🥀",
        "description": "Faded flora with botanical potential.",
        "use": "Can be studied or used in crafting recipes."
    },
    "Fresh Carrots": {
        "rarity": "Rare", "category": "food", "icon": "🥕",
        "description": "Crisp and delicious cave harvest.",
        "use": "Provides high nourishment and trade value."
    },
    "Roses": {
        "rarity": "Rare", "category": "material", "icon": "🌹",
        "description": "Fragrant and beautiful rare flora.",
        "use": "Admire its beauty or trade for rare goods."
    },
    "Perfect Soil": {
        "rarity": "Rare", "category": "material", "icon": "✨",
        "description": "Pristine, glowing earth.",
        "use": "Instantly fulfills Fine dirt recipe requirements and unlocks the crafting tree!"
    },
    "Compound Dirt": {
        "rarity": "Crafted", "category": "crafted", "icon": "🧱",
        "description": "An upgraded composite soil block.",
        "use": "Used for sturdy underground foundations."
    },
    "Fine dirt": {
        "rarity": "Crafted", "category": "crafted", "icon": "🟫",
        "description": "Ultra-smooth silt.",
        "use": "Primary foundation for building high-tier stone structures like the Stone Oven."
    },
    "Pebble Axe": {
        "rarity": "Crafted", "category": "tool", "icon": "🪓",
        "description": "A crude stone axe tied with roots.",
        "use": "Passive Tool: Permanently multiplies materials harvested when digging!"
    },
    "Stone Oven": {
        "rarity": "Crafted", "category": "tool", "icon": "🔥",
        "description": "A hearth built from fine dirt and pebbles.",
        "use": "Culinary Station: Unlocks heat processing and advanced cave baking."
    }
}

def set_top_right_message(text):
    st.session_state.message = text
    st.session_state.message_expiry = time.time() + 2.0

def perform_dig():
    tool_mult = st.session_state.tool_boosters.get("Pebble Axe", {}).get("multiplier", 2) if st.session_state.inventory.get("Pebble Axe", 0) > 0 else 1
    roll = random.random()
    if roll < 0.50:
        item = random.choice(["Dirt", "Worms", "Roots"])
    elif roll < 0.75:
        item = "Pebbles"
    elif roll < 0.90:
        item = random.choice(["Soil", "Old Carrots", "Dead Flower"])
    else:
        item = random.choice(["Fresh Carrots", "Roses", "Perfect Soil"])
        
    st.session_state.inventory[item] += tool_mult
    if tool_mult > 1:
        set_top_right_message(f"+{tool_mult}x {item} (Tool Booster!)")
    else:
        set_top_right_message(f"+1 {item}")

# Define Inventory Modal using Streamlit's native dialog decorator
@st.dialog("🎒 Backpack Inventory", width="large")
def inventory_modal():
    # Category Tabs
    tab_cols = st.columns(5)
    categories = [("all", "All"), ("material", "Materials"), ("food", "Food"), ("crafted", "Crafted"), ("tool", "Tools")]
    for i, (cat_key, cat_label) in enumerate(categories):
        with tab_cols[i]:
            if st.button(cat_label, key=f"tab_btn_{cat_key}"):
                st.session_state.inv_tab = cat_key
                st.rerun()

    st.markdown("---")

    # Sorting Controls
    sort_col1, sort_col2 = st.columns(2)
    with sort_col1:
        st.session_state.inv_sort_by = st.selectbox("Sort by", ["Rarity", "Name", "Amount"], key="sort_by_select")
    with sort_col2:
        st.session_state.inv_sort_order = st.selectbox("Order", ["Standard (Ascending)", "Reverse (Descending)"], key="sort_order_select")

    st.markdown("---")

    # Filter and Sort Items (Only show discovered items with count > 0)
    items_to_display = []
    rarity_weight = {"Common": 1, "Uncommon": 2, "Rare": 3, "Crafted": 4}

    for item_name, count in st.session_state.inventory.items():
        if count <= 0:
            continue
            
        meta = ITEM_ENCYCLOPEDIA.get(item_name, {"rarity": "Common", "category": "material", "icon": "📦", "description": "Unknown item.", "use": "Unknown use."})
        if st.session_state.inv_tab != "all" and meta["category"] != st.session_state.inv_tab:
            continue
        items_to_display.append({
            "name": item_name,
            "count": count,
            "rarity": meta["rarity"],
            "rarity_weight": rarity_weight.get(meta["rarity"], 1),
            "icon": meta["icon"],
            "description": meta["description"],
            "use": meta["use"]
        })

    # Apply Sorting
    reverse_bool = "Reverse" in st.session_state.inv_sort_order
    if st.session_state.inv_sort_by == "Name":
        items_to_display.sort(key=lambda x: x["name"], reverse=reverse_bool)
    elif st.session_state.inv_sort_by == "Amount":
        items_to_display.sort(key=lambda x: x["count"], reverse=reverse_bool)
    else: # Rarity
        items_to_display.sort(key=lambda x: x["rarity_weight"], reverse=reverse_bool)

    # Render Grid using Streamlit Buttons
    if not items_to_display:
        st.info("No discovered items in this category yet. Go dig in the cave!")
    else:
        cols_per_row = 4
        rows = [items_to_display[i:i + cols_per_row] for i in range(0, len(items_to_display), cols_per_row)]
        
        for row in rows:
            cols = st.columns(cols_per_row)
            for idx, item in enumerate(row):
                with cols[idx]:
                    button_label = f"{item['icon']} {item['name']}\n📦 x{item['count']}"
                    if st.button(button_label, key=f"inv_click_{item['name']}", help=f"{item['description']}\n\nUse: {item['use']}"):
                        st.session_state.selected_item = item['name']
                        st.session_state.show_inventory_modal = False
                        st.rerun()

# Router
if st.session_state.state == "MENU":
    st.markdown("<h1 style='text-align: center;'>CAVEMAN TYCOON</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Play Now"):
            st.session_state.state = "TUTORIAL"
            st.rerun()
        if st.button("Audio"):
            st.session_state.state = "AUDIO"
            st.rerun()
        if st.button("Performance"):
            st.session_state.state = "PERFORMANCE"
            st.rerun()

elif st.session_state.state == "TUTORIAL":
    st.markdown("<h1>🦴 Welcome to Caveman Tycoon — Tutorial</h1>", unsafe_allow_html=True)
    st.markdown("Click **Open Inventory** in the game arena anytime to view your discovered items! *(Tip: Press **'q'** on your keyboard anytime to open the Admin Panel)*")
    if st.button("🚀 Start Playing!"):
        st.session_state.state = "PLAYING"
        st.rerun()

elif st.session_state.state == "ADMIN":
    st.markdown("<h1>🛠️ Advanced Admin Panel</h1>", unsafe_allow_html=True)
    st.markdown("Manage resources, custom recipes, tool boosters, and global unlocks.")
    st.markdown("---")

    # Global Actions
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if st.button("✨ Unlock All Items & Crafting Tree"):
            for item in st.session_state.inventory:
                if st.session_state.inventory[item] == 0:
                    st.session_state.inventory[item] = 1
            st.success("Unlocked all items and trees!")
            st.rerun()
    with col_g2:
        if st.button("♾️ Enable Unlimited Resources (999x All)"):
            for item in st.session_state.inventory:
                st.session_state.inventory[item] = 999
            st.success("Set all resources to 999!")
            st.rerun()

    st.markdown("---")

    # Tabs for Admin Features
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📦 Give Items & Inventory", "⚡ Tool Boosters (Lv. 1-100)", "🧪 Custom Recipes"])

    with admin_tab1:
        st.markdown("### Item Give / Edit Quantities")
        for item in list(st.session_state.inventory.keys()):
            st.session_state.inventory[item] = st.number_input(
                f"Quantity: {item}", 
                min_value=0, 
                value=int(st.session_state.inventory[item]), 
                key=f"admin_give_{item}"
            )

    with admin_tab2:
        st.markdown("### Tool Level & Booster Configuration (Level 1 - 100)")
        for tool_name in ["Pebble Axe", "Stone Oven"]:
            if tool_name not in st.session_state.tool_boosters:
                st.session_state.tool_boosters[tool_name] = {"level": 1, "multiplier": 2}
            
            st.markdown(f"#### 🛠️ {tool_name}")
            curr_lvl = st.session_state.tool_boosters[tool_name]["level"]
            new_lvl = st.slider(f"Level for {tool_name}", 1, 100, value=curr_lvl, key=f"slider_lvl_{tool_name}")
            
            # Auto scale multiplier based on level
            calculated_mult = new_lvl * 2
            st.session_state.tool_boosters[tool_name]["level"] = new_lvl
            st.session_state.tool_boosters[tool_name]["multiplier"] = calculated_mult
            st.markdown(f"**Current Efficiency Multiplier:** x{calculated_mult}")
            st.markdown("---")

    with admin_tab3:
        st.markdown("### 🧪 Create Custom Recipe")
        with st.form("custom_recipe_form"):
            new_recipe_name = st.text_input("New Recipe / Item Name")
            new_item_rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Crafted"])
            new_item_icon = st.text_input("Icon Emoji", value="📦")
            new_item_desc = st.text_area("Description")
            new_item_use = st.text_area("Use / Effect")
            
            st.markdown("#### Required Ingredient 1")
            ing1_name = st.selectbox("Ingredient 1 Item", list(st.session_state.inventory.keys()), key="ing1")
            ing1_amt = st.number_input("Amount needed", min_value=1, value=1, key="ing1_amt")
            
            submit_recipe = st.form_submit_button("Create & Register Recipe")
            if submit_recipe and new_recipe_name:
                ITEM_ENCYCLOPEDIA[new_recipe_name] = {
                    "rarity": new_item_rarity, "category": "crafted", "icon": new_item_icon,
                    "description": new_item_desc, "use": new_item_use
                }
                if new_recipe_name not in st.session_state.inventory:
                    st.session_state.inventory[new_recipe_name] = 0
                st.session_state.recipes[new_recipe_name] = {ing1_name: ing1_amt}
                st.success(f"Successfully created custom recipe for '{new_recipe_name}'!")

    st.markdown("---")
    if st.button("← Back to Game"):
        st.session_state.state = "PLAYING"
        st.rerun()

elif st.session_state.state == "AUDIO":
    st.markdown("<h1>Audio Settings</h1>", unsafe_allow_html=True)
    if st.button("Back"):
        st.session_state.state = "MENU"
        st.rerun()

elif st.session_state.state == "PERFORMANCE":
    st.markdown("<h1>Performance Settings</h1>", unsafe_allow_html=True)
    if st.button("Back"):
        st.session_state.state = "MENU"
        st.rerun()

elif st.session_state.state == "PLAYING":
    # Check if 'q' key hotkey was pressed via query params
    if st.query_params.get("admin_mode") == "true":
        st.query_params.clear()
        st.session_state.state = "ADMIN"
        st.rerun()

    # Top-right header bar for notifications and menu button
    col_top_left, col_top_right = st.columns([3, 2])
    with col_top_left:
        if st.session_state.message and time.time() < st.session_state.message_expiry:
            st.markdown(f"<div style='text-align: left; font-weight: bold; color: #B45309; padding-top: 8px;'>✨ {st.session_state.message}</div>", unsafe_allow_html=True)
    with col_top_right:
        if st.button("🏠 Menu"):
            st.session_state.state = "MENU"
            st.session_state.show_actions = False
            st.session_state.show_inventory_modal = False
            st.rerun()
            
    st.markdown("---")
    
    # Pastel Blue Recipe Sidebar
    with st.sidebar:
        st.markdown("### 📜 Recipe Book & Crafting")
        st.markdown("---")
        
        has_perfect_soil = st.session_state.inventory.get("Perfect Soil", 0) > 0
        has_crafted_fine_dirt = st.session_state.inventory.get("Fine dirt", 0) > 0
        fine_dirt_unlocked = has_perfect_soil or has_crafted_fine_dirt
        
        has_found_pebbles = st.session_state.inventory.get("Pebbles", 0) > 0
        has_crafted_pebble_axe = st.session_state.inventory.get("Pebble Axe", 0) > 0
        pebble_axe_unlocked = has_found_pebbles or has_crafted_pebble_axe
        
        for recipe_name, recipe_data in st.session_state.recipes.items():
            if recipe_name == "Fine dirt" and not fine_dirt_unlocked:
                continue
            if recipe_name == "Pebble Axe" and not pebble_axe_unlocked:
                continue
                
            st.markdown(f"#### 🧪 {recipe_name}")
            can_craft = False
            chosen_option = None
            
            if "alternatives" in recipe_data:
                for alt in recipe_data["alternatives"]:
                    met = True
                    for ing, req_amt in alt.items():
                        if st.session_state.inventory.get(ing, 0) < req_amt:
                            met = False
                    if met:
                        can_craft = True
                        chosen_option = alt
            else:
                can_craft = True
                for ing, req_amt in recipe_data.items():
                    if st.session_state.inventory.get(ing, 0) < req_amt:
                        can_craft = False
                chosen_option = recipe_data
                
            if can_craft:
                if st.button(f"Craft {recipe_name}", key=f"craft_btn_{recipe_name}"):
                    for ing, req_amt in chosen_option.items():
                        st.session_state.inventory[ing] -= req_amt
                    if recipe_name not in st.session_state.inventory:
                        st.session_state.inventory[recipe_name] = 0
                    st.session_state.inventory[recipe_name] += 1
                    set_top_right_message(f"Crafted {recipe_name}!")
                    st.session_state.show_inventory_modal = False
                    st.rerun()
            else:
                st.markdown("<span style='color: #9B2C2C; font-weight: bold;'>Missing Ingredients ❌</span>", unsafe_allow_html=True)
            st.markdown("---")

    # Main Game Area with Inventory Pop-up Trigger Button
    col_main = st.columns(1)[0]
    with col_main:
        if st.button("🎒 Open Inventory"):
            st.session_state.show_inventory_modal = True
            st.rerun()

        # Trigger the modal conditionally based on flag
        if st.session_state.show_inventory_modal:
            inventory_modal()
            
        # Display currently selected item if any
        if st.session_state.selected_item:
            sel = st.session_state.selected_item
            info = ITEM_ENCYCLOPEDIA.get(sel, {})
            st.info(f"📌 **Selected Item:** {info.get('icon', '📦')} {sel} (Owned: {st.session_state.inventory.get(sel, 0)}) — {info.get('use', '')}")

        st.markdown("<br>", unsafe_allow_html=True)
        play_tab1, play_tab2, play_tab3 = st.tabs(["⛏️ Cave", "🌳 Craft Tree", "📖 Items Book"])
        
        with play_tab1:
            st.markdown("<h3 style='text-align: center;'>The Great Cave</h3>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Actions", key="actions_btn"):
                st.session_state.show_actions = not st.session_state.show_actions
                st.session_state.show_inventory_modal = False
                st.rerun()
            
            if st.session_state.show_actions:
                st.markdown("### Choose Action:")
                if st.button("⛏️ Dig"):
                    perform_dig()
                    st.session_state.show_inventory_modal = False
                    st.rerun()

        with play_tab2:
            st.markdown("### 🌳 Progression Craft Tree")
            st.markdown("Unlock milestones, upgrade tool efficiencies, and view your caveman advancement tree below:")
            st.markdown("<br>", unsafe_allow_html=True)

            # Feature 1: Compound Dirt Tier
            st.markdown("""
                <div class="craft-node">
                    <h4>🧱 Tier 1: Compound Foundations</h4>
                    <p><b>Requirement:</b> 3x Dirt, 2x Worms</p>
                    <p><b>Effect:</b> Unlocks sturdy groundwork blocks for cave settlement.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Feature 2: Pebble Axe Tier
            st.markdown("""
                <div class="craft-node">
                    <h4>🪓 Tier 2: Pebble Axe Tool</h4>
                    <p><b>Requirement:</b> 4x Pebbles, 3x Roots</p>
                    <p><b>Effect:</b> Permanently boosts digging yields based on your tool level!</p>
                </div>
            """, unsafe_allow_html=True)

            # Feature 3: Fine Dirt & Stone Oven Tier
            st.markdown("""
                <div class="craft-node">
                    <h4>🔥 Tier 3: Stone Oven & Hearth</h4>
                    <p><b>Requirement:</b> 2x Fine dirt, 10x Pebbles</p>
                    <p><b>Effect:</b> Unlocks advanced culinary baking and heat processing stations.</p>
                </div>
            """, unsafe_allow_html=True)

        with play_tab3:
            st.markdown("### 📖 Items Book (Discovery Codex)")
            for item_name, info in ITEM_ENCYCLOPEDIA.items():
                if st.session_state.inventory.get(item_name, 0) > 0:
                    with st.expander(f"✨ {item_name} ({info['rarity']})"):
                        st.markdown(f"**Owned:** {st.session_state.inventory.get(item_name, 0)}")
                        st.markdown(f"🎯 **Use:** {info['use']}")
                else:
                    with st.container(border=True):
                        st.markdown(f"<span class='item-shadow'>🔒 ???</span>", unsafe_allow_html=True)

    # Auto-refresh mechanism to clear top-right notification after 2 seconds
    if st.session_state.message and time.time() < st.session_state.message_expiry:
        time.sleep(0.5)
        st.rerun()
    elif st.session_state.message and time.time() >= st.session_state.message_expiry:
        st.session_state.message = ""