# app.py
import streamlit as st
import random
import time
from data import ITEM_ENCYCLOPEDIA, DEFAULT_RECIPES
from components import inventory_modal

# Page configuration
st.set_page_config(
    page_title="Caveman Tycoon",
    page_icon="🦴",
    layout="wide"
)

# Initialize Session State variables
if "state" not in st.session_state:
    st.session_state.state = "MENU"

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Dirt": 0, "Worms": 0, "Roots": 0, "Pebbles": 0, "Coal": 0,
        "Soil": 0, "Old Carrots": 0, "Dead Flower": 0,
        "Fresh Carrots": 0, "Roses": 0, "Perfect Soil": 0, "Metal Fragments": 0,
        "Compound Dirt": 0, "Fine dirt": 0, "Molten Metal": 0,
        "Pebble Axe": 0, "Stone Oven": 0
    }

if "recipes" not in st.session_state:
    st.session_state.recipes = DEFAULT_RECIPES

if "tool_boosters" not in st.session_state:
    st.session_state.tool_boosters = {
        "Pebble Axe": {"level": 1, "multiplier": 2},
        "Stone Oven": {"level": 1, "multiplier": 1}
    }

if "ui_settings" not in st.session_state:
    st.session_state.ui_settings = {
        "bg_color": "#FEF3C7",
        "text_color": "#92400E",
        "border_color": "#F59E0B"
    }

if "item_custom_colors" not in st.session_state:
    st.session_state.item_custom_colors = {item: data.get("color", "#F0F0F0") for item, data in ITEM_ENCYCLOPEDIA.items()}

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

# Custom CSS with fixed tooltip sizing and appearance
ui = st.session_state.ui_settings
st.markdown(f"""
<style>
    .stApp {{
        background-color: #F5EBDC;
        color: #32281E;
    }}
    h1, h2, h3 {{
        color: #78552D !important;
        font-family: Arial, sans-serif;
    }}
    [data-testid="stSidebar"] {{
        background-color: #E3EEF8;
        border-right: 2px solid #A2C4E0;
    }}
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: #1A365D !important;
    }}
    .stButton>button {{
        background-color: #78552D;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #B46E32;
        color: white;
    }}
    .item-shadow {{
        color: rgba(0, 0, 0, 0.25);
        text-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
        filter: blur(1.5px);
        user-select: none;
    }}
    .craft-node {{
        background-color: #EEDCC5;
        border: 2px solid #B46E32;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }}
    .dig-popup {{
        background-color: {ui['bg_color']};
        color: {ui['text_color']};
        border: 2px solid {ui['border_color']};
        padding: 12px 18px;
        border-radius: 10px;
        font-size: 1.15rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        margin-top: 5px;
    }}
    /* Fixed Tooltip styling to prevent empty boxes */
    .recipe-tooltip {{
        position: relative;
        display: block;
        cursor: pointer;
    }}
    .recipe-tooltip .tooltip-text {{
        visibility: hidden;
        width: 230px;
        background-color: #1A365D;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 999;
        bottom: 125%;
        left: 0;
        opacity: 0;
        transition: opacity 0.3s ease;
        transition-delay: 0.5s;
        font-size: 0.85rem;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
        pointer-events: none;
    }}
    .recipe-tooltip:hover .tooltip-text {{
        visibility: visible;
        opacity: 1;
    }}
</style>
""", unsafe_allow_html=True)

# JavaScript Hotkey Listener
st.markdown("""
<script>
    document.addEventListener('keydown', function(event) {
        if (event.key.toLowerCase() === 'q' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            event.preventDefault();
            const url = new URL(window.location.href);
            url.searchParams.set('admin_mode', 'true');
            window.location.href = url.toString();
        }
    });
</script>
""", unsafe_allow_html=True)

def set_notification(text):
    st.session_state.message = text
    st.session_state.message_expiry = time.time() + 2.5

def perform_dig():
    tool_mult = st.session_state.tool_boosters.get("Pebble Axe", {}).get("multiplier", 2) if st.session_state.inventory.get("Pebble Axe", 0) > 0 else 1
    roll = random.random()
    if roll < 0.40:
        item = random.choice(["Dirt", "Worms", "Roots"])
    elif roll < 0.65:
        item = random.choice(["Pebbles", "Coal"])
    elif roll < 0.85:
        item = random.choice(["Soil", "Old Carrots", "Dead Flower"])
    else:
        item = random.choice(["Fresh Carrots", "Roses", "Perfect Soil", "Metal Fragments"])
        
    st.session_state.inventory[item] += tool_mult
    meta = ITEM_ENCYCLOPEDIA.get(item, {"icon": "📦"})
    icon = meta["icon"]
    
    if tool_mult > 1:
        set_notification(f"✨ +{tool_mult}x {icon} {item} (Tool Boost!)")
    else:
        set_notification(f"✨ +1 {icon} {item}")

# Router
if st.session_state.state == "MENU":
    st.markdown("<h1 style='text-align: center;'>CAVEMAN TYCOON</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Play Now"):
            st.session_state.state = "TUTORIAL"
            st.rerun()
        if st.button("Interface Settings"):
            st.session_state.state = "SETTINGS"
            st.rerun()
        if st.button("Audio"):
            st.session_state.state = "AUDIO"
            st.rerun()
        if st.button("Performance"):
            st.session_state.state = "PERFORMANCE"
            st.rerun()

elif st.session_state.state == "SETTINGS":
    st.markdown("<h1>⚙️ Interface & Material Color Settings</h1>", unsafe_allow_html=True)
    st.markdown("Customize your general notification highlights and individual item background colors.")
    st.markdown("---")
    
    st.session_state.ui_settings["bg_color"] = st.color_picker("Notification Highlight Background Color", st.session_state.ui_settings["bg_color"])
    st.session_state.ui_settings["text_color"] = st.color_picker("Notification Text Color", st.session_state.ui_settings["text_color"])
    st.session_state.ui_settings["border_color"] = st.color_picker("Notification Border Color", st.session_state.ui_settings["border_color"])

    st.markdown("### 🎨 Individual Material Card Colors")
    for item_name in ITEM_ENCYCLOPEDIA:
        curr_color = st.session_state.item_custom_colors.get(item_name, "#F0F0F0")
        st.session_state.item_custom_colors[item_name] = st.color_picker(f"Background color for {item_name}", curr_color, key=f"color_picker_{item_name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Menu"):
        st.session_state.state = "MENU"
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
                    "description": new_item_desc, "use": new_item_use, "color": "#E0E0E0"
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
    if st.query_params.get("admin_mode") == "true":
        st.query_params.clear()
        st.session_state.state = "ADMIN"
        st.rerun()

    col_top_left, col_top_right = st.columns([3, 2])
    with col_top_right:
        if st.button("🏠 Menu"):
            st.session_state.state = "MENU"
            st.session_state.show_actions = False
            st.session_state.show_inventory_modal = False
            st.rerun()
            
    st.markdown("---")
    
    with st.sidebar:
        st.markdown("### 📜 Recipe Book & Crafting")
        st.markdown("---")
        
        has_perfect_soil = st.session_state.inventory.get("Perfect Soil", 0) > 0
        has_crafted_fine_dirt = st.session_state.inventory.get("Fine dirt", 0) > 0
        fine_dirt_unlocked = has_perfect_soil or has_crafted_fine_dirt
        
        has_found_pebbles = st.session_state.inventory.get("Pebbles", 0) > 0
        has_crafted_pebble_axe = st.session_state.inventory.get("Pebble Axe", 0) > 0
        pebble_axe_unlocked = has_found_pebbles or has_crafted_pebble_axe

        has_stone_oven = st.session_state.inventory.get("Stone Oven", 0) > 0
        
        for recipe_name, recipe_data in st.session_state.recipes.items():
            if recipe_name == "Fine dirt" and not fine_dirt_unlocked:
                continue
            if recipe_name == "Pebble Axe" and not pebble_axe_unlocked:
                continue
            if recipe_name == "Molten Metal" and not has_stone_oven:
                continue
                
            # Build recipe lines with check marks (✔) and crosses (❌) based on inventory
            tooltip_lines = []
            if "alternatives" in recipe_data:
                alt_block = []
                for alt in recipe_data["alternatives"]:
                    sub_lines = []
                    for ing, req_amt in alt.items():
                        owned = st.session_state.inventory.get(ing, 0)
                        symbol = "✔" if owned >= req_amt else "❌"
                        sub_lines.append(f"{symbol} {req_amt}x {ing} (Have: {owned})")
                    alt_block.append(" or ".join(sub_lines))
                tooltip_lines.append(" / ".join(alt_block))
            else:
                for ing, req_amt in recipe_data.items():
                    owned = st.session_state.inventory.get(ing, 0)
                    symbol = "✔" if owned >= req_amt else "❌"
                    tooltip_lines.append(f"{symbol} {req_amt}x {ing} (Have: {owned})")
            
            recipe_string = "<br>".join(tooltip_lines)

            # Render item title with hover tooltip wrapper
            st.markdown(f"""
                <div class="recipe-tooltip">
                    <h4 style="margin-bottom: 2px;">🧪 {recipe_name}</h4>
                    <div class="tooltip-text"><b>Recipe Requirements:</b><br>{recipe_string}</div>
                </div>
            """, unsafe_allow_html=True)

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
                    meta = ITEM_ENCYCLOPEDIA.get(recipe_name, {"icon": "📦"})
                    set_notification(f"🎉 Crafted {meta['icon']} {recipe_name}!")
                    st.session_state.show_inventory_modal = False
                    st.rerun()
            else:
                st.markdown("<span style='color: #9B2C2C; font-weight: bold;'>Missing Ingredients ❌</span>", unsafe_allow_html=True)
            st.markdown("---")

    col_main = st.columns(1)[0]
    with col_main:
        if st.button("🎒 Open Inventory"):
            st.session_state.show_inventory_modal = True
            st.rerun()

        if st.session_state.show_inventory_modal:
            inventory_modal()
            
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
                
                col_dig, col_popup = st.columns([1, 2])
                with col_dig:
                    if st.button("⛏️ Dig"):
                        perform_dig()
                        st.session_state.show_inventory_modal = False
                        st.rerun()
                with col_popup:
                    if st.session_state.message and time.time() < st.session_state.message_expiry:
                        st.markdown(f"<div class='dig-popup'>{st.session_state.message}</div>", unsafe_allow_html=True)

        with play_tab2:
            st.markdown("### 🌳 Progression Craft Tree")
            st.markdown("Unlock milestones, upgrade tool efficiencies, and view your caveman advancement tree below:")
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
                <div class="craft-node">
                    <h4>🧱 Tier 1: Compound Foundations</h4>
                    <p><b>Requirement:</b> 3x Dirt, 2x Worms</p>
                    <p><b>Effect:</b> Unlocks sturdy groundwork blocks for cave settlement.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="craft-node">
                    <h4>🪓 Tier 2: Pebble Axe Tool</h4>
                    <p><b>Requirement:</b> 4x Pebbles, 3x Roots</p>
                    <p><b>Effect:</b> Permanently boosts digging yields based on your tool level!</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="craft-node">
                    <h4>🔥 Tier 3: Stone Oven & Smelting</h4>
                    <p><b>Requirement:</b> 2x Fine dirt, 10x Pebbles</p>
                    <p><b>Effect:</b> Unlocks the Stone Oven to smelt Metal Fragments and Coal into Molten Metal!</p>
                </div>
            """, unsafe_allow_html=True)

        with play_tab3:
            st.markdown("### 📖 Items Book (Discovery Codex)")
            for item_name, info in ITEM_ENCYCLOPEDIA.items():
                if st.session_state.inventory.get(item_name, 0) > 0:
                    item_bg_color = st.session_state.item_custom_colors.get(item_name, info.get("color", "#F0F0F0"))
                    with st.expander(f"✨ {item_name} ({info['rarity']})"):
                        st.markdown(f"""
                            <div style="background-color: {item_bg_color}; padding: 8px; border-radius: 6px; margin-bottom: 5px;">
                                <b>Owned:</b> {st.session_state.inventory.get(item_name, 0)}<br>
                                🎯 <b>Use:</b> {info['use']}
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    with st.container(border=True):
                        st.markdown(f"<span class='item-shadow'>🔒 ???</span>", unsafe_allow_html=True)

    if st.session_state.message and time.time() < st.session_state.message_expiry:
        time.sleep(0.5)
        st.rerun()
    elif st.session_state.message and time.time() >= st.session_state.message_expiry:
        st.session_state.message = ""