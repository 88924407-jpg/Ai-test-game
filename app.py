# app.py
import importlib
import streamlit as st
import streamlit.components.v1 as components
import random
import time

import data as game_data

if not all(
    hasattr(game_data, name)
    for name in ("CRAFT_TREE_BRANCHES", "CRAFT_TREE_ITEMS")
):
    existing_encyclopedia = game_data.ITEM_ENCYCLOPEDIA
    game_data = importlib.reload(game_data)
    existing_encyclopedia.update(game_data.ITEM_ENCYCLOPEDIA)
    game_data.ITEM_ENCYCLOPEDIA = existing_encyclopedia

CRAFT_TREE_BRANCHES = game_data.CRAFT_TREE_BRANCHES
CRAFT_TREE_ITEMS = game_data.CRAFT_TREE_ITEMS
CRAFT_TREE_PAPERS = game_data.CRAFT_TREE_PAPERS
DEFAULT_RECIPES = game_data.DEFAULT_RECIPES
ITEM_ENCYCLOPEDIA = game_data.ITEM_ENCYCLOPEDIA

from components import (
    PIXEL_ICON_CHOICES,
    icon_button_style as render_icon_button_style,
    icon_text as render_icon_text,
    inventory_modal,
    paper_drawing_html as render_paper_drawing_html,
    pixel_icon_html as render_pixel_icon_html,
    replace_icons,
    safe_widget_key,
)

BACKPACK_CAPACITY = 200
DEFAULT_STORAGE_CAPACITY = 100

# Page configuration
st.set_page_config(
    page_title="Caveman Tycoon",
    page_icon="assets/caveman-icon.svg",
    layout="wide"
)

# Initialize Session State variables
if "state" not in st.session_state:
    st.session_state.state = "MENU"

if "inventory" not in st.session_state:
    st.session_state.inventory = dict.fromkeys(ITEM_ENCYCLOPEDIA, 0)
for item_name in ITEM_ENCYCLOPEDIA:
    st.session_state.inventory.setdefault(item_name, 0)

if "storage" not in st.session_state:
    st.session_state.storage = dict.fromkeys(ITEM_ENCYCLOPEDIA, 0)
for item_name in ITEM_ENCYCLOPEDIA:
    st.session_state.storage.setdefault(item_name, 0)

st.session_state.setdefault("storage_built", False)
st.session_state.setdefault("storage_capacity", DEFAULT_STORAGE_CAPACITY)
st.session_state.setdefault("storage_category", "all")
st.session_state.setdefault("storage_horizontal", True)
st.session_state.setdefault("unlocked_craft_branches", [])
st.session_state.setdefault("mouse_insulation_level", 0)
st.session_state.setdefault("mouse_repellent_level", 0)
st.session_state.setdefault("mice_raid_pending", False)
st.session_state.setdefault("mice_raid_deadline", 0.0)

if "recipes" not in st.session_state:
    st.session_state.recipes = dict(DEFAULT_RECIPES)
for recipe_name, recipe_data in DEFAULT_RECIPES.items():
    st.session_state.recipes.setdefault(recipe_name, recipe_data)

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
st.session_state.ui_settings.setdefault("theme", "Forest")
st.session_state.ui_settings.setdefault("art_style", "Advanced Simple")
st.session_state.setdefault("game_page", "Cave")
if st.session_state.game_page not in ("Cave", "Craft Tree", "Items Book", "Camp"):
    st.session_state.game_page = "Cave"
game_groups = {
    "Explore": ("Cave", "Craft Tree"),
    "Collection": ("Items Book",),
    "Settlement": ("Camp",),
}
page_groups = {
    page: group for group, pages in game_groups.items() for page in pages
}
st.session_state.setdefault("game_group", page_groups[st.session_state.game_page])
if st.session_state.game_group not in game_groups:
    st.session_state.game_group = page_groups[st.session_state.game_page]
elif st.session_state.game_page not in game_groups[st.session_state.game_group]:
    st.session_state.game_page = game_groups[st.session_state.game_group][0]

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

# Shared visual theme
ui = st.session_state.ui_settings
visual_themes = {
    "Forest": {
        "earth_900": "#263A35",
        "earth_700": "#3F6255",
        "earth_600": "#6B8060",
        "muted": "#68746B",
        "paper": "#F7F5ED",
        "line": "#D7DCCF",
        "accent": "#C58A45",
        "accent_soft": "#F1E5CF",
        "background": "#EFF1E8",
        "sidebar": "#E8ECE2",
        "hero_start": "#E2E9DC",
        "button_start": "#527565",
        "button_end": "#34564A",
        "button_hover": "#678B70",
    },
    "Cavern": {
        "earth_900": "#303B49",
        "earth_700": "#4C6175",
        "earth_600": "#718398",
        "muted": "#687580",
        "paper": "#F1F3F4",
        "line": "#D2D9DF",
        "accent": "#B98B55",
        "accent_soft": "#EEE5D8",
        "background": "#E9EEF1",
        "sidebar": "#DFE7EB",
        "hero_start": "#DFE8EC",
        "button_start": "#60798D",
        "button_end": "#3E586D",
        "button_hover": "#7691A5",
    },
    "Ember": {
        "earth_900": "#49352F",
        "earth_700": "#755346",
        "earth_600": "#98715A",
        "muted": "#7C6A60",
        "paper": "#FAF2EA",
        "line": "#E2D4C7",
        "accent": "#C27443",
        "accent_soft": "#F3E2D1",
        "background": "#F2EAE2",
        "sidebar": "#EAE0D7",
        "hero_start": "#F0E0D2",
        "button_start": "#98674F",
        "button_end": "#704A3C",
        "button_hover": "#AD795D",
    },
}
if ui["theme"] not in visual_themes:
    ui["theme"] = "Forest"
if ui["art_style"] not in ("Advanced Simple", "Pixel Art", "Soft Illustrated"):
    ui["art_style"] = "Advanced Simple"
theme = visual_themes.get(ui["theme"], visual_themes["Forest"])
art_style = ui["art_style"]
st.markdown(f"""
<style>
    :root {{
        --earth-900: {theme['earth_900']};
        --earth-700: {theme['earth_700']};
        --earth-600: {theme['earth_600']};
        --muted: {theme['muted']};
        --paper: {theme['paper']};
        --line: {theme['line']};
        --accent: {theme['accent']};
        --accent-soft: {theme['accent_soft']};
        --page-background: {theme['background']};
        --sidebar-background: {theme['sidebar']};
        --hero-start: {theme['hero_start']};
        --button-start: {theme['button_start']};
        --button-end: {theme['button_end']};
        --button-hover: {theme['button_hover']};
    }}
    .stApp {{
        background:
            radial-gradient(ellipse at 12% 0%, rgba(190, 202, 174, 0.38), transparent 35rem),
            radial-gradient(ellipse at 100% 18%, rgba(226, 203, 163, 0.20), transparent 30rem),
            var(--page-background);
        color: var(--earth-900);
    }}
    [data-testid="stAppViewContainer"] .main .block-container {{
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}
    p, label {{
        color: var(--earth-900);
    }}
    h1, h2, h3, h4 {{
        color: var(--earth-900) !important;
        font-family: "Trebuchet MS", Arial, sans-serif;
        letter-spacing: -0.025em;
    }}
    h1 {{ font-size: clamp(2rem, 3.2vw, 2.8rem) !important; }}
    hr {{ border-color: var(--line); }}
    [data-testid="stSidebar"] {{
        background: var(--sidebar-background);
        border-right: 1px solid var(--line);
    }}
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {{
        color: var(--earth-900) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: var(--muted);
        font-size: 0.91rem;
    }}
    [data-testid="stTabs"] [role="tablist"] {{
        gap: 0.5rem;
        border-bottom: 1px solid var(--line);
    }}
    [data-testid="stTabs"] button[role="tab"] {{
        border-radius: 9px 9px 0 0;
        color: var(--muted);
        font-weight: 650;
        padding: 0.65rem 1rem;
        transition: background-color 140ms ease, color 140ms ease;
    }}
    [data-testid="stTabs"] button[role="tab"]:hover {{
        background: #E6EADF;
        color: var(--earth-900);
    }}
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        background: #DCE7D8;
        color: var(--earth-900);
    }}
    [data-testid="stExpander"] {{
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
    }}
    [data-testid="stMetric"] {{
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 0.8rem 1rem;
    }}
    [data-testid="stMetricLabel"] {{ color: var(--muted); }}
    [data-testid="stMetricValue"] {{ color: var(--earth-700); }}
    [data-baseweb="input"], [data-baseweb="select"], [data-baseweb="textarea"] {{
        border-radius: 8px;
    }}
    .stButton>button {{
        background: linear-gradient(145deg, var(--button-start), var(--button-end));
        color: #F8F7F0;
        border: 1px solid #72896B;
        border-bottom: 3px solid #263A35;
        border-radius: 11px;
        padding: 0.68rem 1rem;
        font-weight: 650;
        width: 100%;
        box-shadow: 0 3px 0 rgba(38, 58, 53, 0.12), 0 5px 12px rgba(38, 58, 53, 0.08);
        transition: background 160ms ease, border-color 160ms ease, transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
    }}
    .stButton>button:hover {{
        background: linear-gradient(145deg, var(--button-hover), var(--earth-700));
        border-color: #9BA77B;
        color: #FFFFFF;
        box-shadow: 0 4px 0 rgba(38, 58, 53, 0.12), 0 8px 18px rgba(38, 58, 53, 0.18);
        filter: saturate(1.08);
        transform: translateY(-2px) scale(1.01);
    }}
    .stButton>button:active {{
        box-shadow: 0 1px 0 rgba(38, 58, 53, 0.14);
        transform: translateY(1px) scale(0.99);
    }}
    .stButton>button:focus-visible {{
        outline: 3px solid #D5A85F;
        outline-offset: 3px;
    }}
    .stButton>button:disabled {{
        background: #E1E5DA;
        border-color: #D0D7CA;
        border-bottom-color: #BEC8B9;
        box-shadow: none;
        color: #778177;
        filter: none;
        transform: none;
    }}
    .pixel-icon {{
        image-rendering: auto;
        vertical-align: middle;
        filter: drop-shadow(0 2px 3px rgba(38, 58, 53, 0.14));
    }}
    .illustrated-paper {{
        display: block;
        margin: 0.2rem auto 0.55rem;
        filter: drop-shadow(0 4px 5px rgba(38, 58, 53, 0.14));
        transition: transform 180ms ease, filter 180ms ease;
    }}
    .illustrated-paper:hover {{
        filter: drop-shadow(0 6px 8px rgba(38, 58, 53, 0.22));
        transform: translateY(-3px) rotate(-2deg);
    }}
    .pixel-label {{
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        color: var(--earth-900);
    }}
    [data-testid="stTabs"] button[role="tab"] {{
        border: 1px solid transparent;
        transition: background-color 160ms ease, color 160ms ease, transform 160ms ease;
    }}
    [data-testid="stTabs"] button[role="tab"]:hover {{
        transform: translateY(-2px);
    }}
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        border-color: #C6D3C0;
        box-shadow: inset 0 -3px 0 var(--accent);
    }}
    .st-key-admin-hotkey {{
        position: fixed;
        left: -10000px;
        top: 0;
        width: 1px;
        height: 1px;
        overflow: hidden;
    }}
    .st-key-admin-unlock-card, .st-key-admin-unlimited-card {{
        border-radius: 12px;
        padding: 1rem 1.15rem 0.3rem;
        margin-bottom: 0.8rem;
    }}
    .st-key-admin-unlock-card {{
        background: #E4EDE0;
        border: 1px solid #C2D3B7;
        border-top: 4px solid #6B8060;
    }}
    .st-key-admin-unlock-card .stButton button {{
        background: #55744D;
        border-color: #55744D;
    }}
    .st-key-admin-unlock-card .stButton button:hover {{
        background: #435F3D;
        border-color: #435F3D;
    }}
    .st-key-admin-unlimited-card {{
        background: #E9EBE4;
        border: 1px solid #CDD2C3;
        border-top: 4px solid #8B795D;
    }}
    .st-key-admin-unlimited-card .stButton button {{
        background: #756448;
        border-color: #756448;
    }}
    .st-key-admin-unlimited-card .stButton button:hover {{
        background: #5E5039;
        border-color: #5E5039;
    }}
    .admin-tab-intro {{
        border-radius: 10px;
        padding: 12px 16px;
        margin: 4px 0 16px;
        font-weight: 600;
    }}
    .admin-inventory-intro {{
        background: #E8EEEA;
        border-left: 4px solid #6B8C79;
        color: #344E43;
    }}
    .admin-booster-intro {{
        background: #F3EBDD;
        border-left: 4px solid var(--accent);
        color: #654B2C;
    }}
    .admin-recipe-intro {{
        background: #ECEBE2;
        border-left: 4px solid #8B795D;
        color: #514B3C;
    }}
    .item-shadow {{
        color: rgba(0, 0, 0, 0.25);
        text-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
        filter: blur(1.5px);
        user-select: none;
    }}
    .craft-node {{
        background-color: #E4E8D9;
        border: 2px solid #82916D;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }}
    .craft-tree-hero {{
        background: linear-gradient(115deg, var(--hero-start), var(--paper) 72%);
        border: 1px solid var(--line);
        border-radius: 14px;
        color: var(--earth-900);
        padding: 22px 26px;
        margin: 0 0 18px;
    }}
    .craft-tree-hero h3 {{
        color: var(--earth-900) !important;
        margin: 0 0 6px;
    }}
    .craft-tree-hero p {{
        color: var(--muted);
        margin: 0;
    }}
    .craft-tree-stat {{
        display: inline-block;
        background: var(--accent-soft);
        border: 1px solid #E5D6BC;
        border-radius: 999px;
        padding: 6px 10px;
        margin: 14px 7px 0 0;
        color: var(--earth-700);
        font-size: 0.76rem;
        font-weight: 650;
    }}
    .craft-path-card {{
        position: relative;
        background: var(--paper);
        border: 1px solid var(--line);
        border-top: 3px solid var(--earth-600);
        border-radius: 12px;
        min-height: 205px;
        padding: 17px 16px;
        box-shadow: 0 4px 12px rgba(67, 52, 34, 0.06);
    }}
    .craft-path-icon {{
        font-size: 1.8rem;
        line-height: 1;
    }}
    .craft-path-kicker {{
        color: var(--earth-600);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 14px;
        text-transform: uppercase;
    }}
    .craft-path-card h4 {{
        color: var(--earth-900);
        margin: 4px 0 8px;
    }}
    .craft-path-card p {{
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.45;
        min-height: 40px;
        margin: 0 0 14px;
    }}
    .craft-path-status {{
        display: inline-block;
        background: #E7EBE2;
        border-radius: 999px;
        color: var(--earth-700);
        font-size: 0.75rem;
        font-weight: 650;
        padding: 5px 9px;
    }}
    .craft-branch-label {{
        color: var(--earth-700);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin: 8px 0 12px;
        text-transform: uppercase;
    }}
    .page-hero {{
        background: linear-gradient(115deg, #E2E9DC, #F7F5ED 72%);
        border: 1px solid var(--line);
        border-left: 4px solid var(--accent);
        border-radius: 14px;
        padding: 22px 26px;
        margin: 0 0 22px;
    }}
    .page-hero h1, .page-hero h2, .page-hero h3 {{ margin: 0 0 0.4rem; }}
    .page-hero p {{ color: var(--muted); margin: 0; line-height: 1.55; }}
    .menu-hero {{
        background: linear-gradient(145deg, var(--hero-start) 0%, var(--paper) 72%);
        border: 1px solid var(--line);
        border-radius: 18px;
        margin: 2rem auto 1.2rem;
        padding: 2.4rem 2rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(67, 52, 34, 0.07);
    }}
    .menu-mark {{ font-size: 2.3rem; margin-bottom: 0.4rem; }}
    .menu-hero h1 {{ color: var(--earth-900) !important; margin: 0; }}
    .menu-hero p {{ color: var(--muted); font-size: 1.05rem; margin: 0.55rem 0 0; }}
    .game-header {{
        border-bottom: 1px solid var(--line);
        margin-bottom: 1rem;
        padding: 0 0 1rem;
    }}
    .game-page-heading {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(110deg, var(--hero-start), var(--paper));
        border: 1px solid var(--line);
        border-left: 4px solid var(--accent);
        border-radius: 12px;
        padding: 0.65rem 1rem;
        margin: 0.3rem 0 1.15rem;
        animation: page-arrive 220ms ease-out both;
    }}
    .game-page-heading > span:last-child {{
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.1em;
    }}
    @keyframes page-arrive {{
        from {{ opacity: 0; transform: translateY(5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .game-header h2 {{ margin: 0; }}
    .game-header p {{ color: var(--muted); margin: 0.2rem 0 0; }}
    .cave-panel {{
        background: linear-gradient(135deg, var(--hero-start), var(--paper));
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 20px 24px;
        margin: 6px 0 18px;
        text-align: center;
    }}
    .cave-panel h3 {{ margin: 0 0 5px; }}
    .cave-panel p {{ color: var(--muted); margin: 0; }}
    .inventory-card {{
        border: 1px solid rgba(63, 88, 70, 0.18);
        border-radius: 11px;
        box-shadow: 0 3px 10px rgba(45, 68, 53, 0.08);
        padding: 13px 10px;
        margin-bottom: 7px;
        text-align: center;
    }}
    .inventory-card {{
        transition: transform 160ms ease, box-shadow 160ms ease;
    }}
    .inventory-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 18px rgba(45, 68, 53, 0.14);
    }}
    .st-key-storage-category-wheel .stButton > button {{
        width: 78px;
        height: 78px;
        margin: 0 auto;
        padding: 0.35rem;
        border-radius: 50%;
        white-space: normal;
        line-height: 1.15;
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
        box-shadow: 0px 5px 16px rgba(38, 58, 53, 0.16);
        margin-top: 5px;
        position: relative;
        overflow: hidden;
        animation: cave-pop 420ms cubic-bezier(0.2, 0.8, 0.2, 1) both,
            cave-glow 1.4s ease-out both;
    }}
    .dig-popup::after {{
        content: "✦";
        position: absolute;
        right: 16px;
        top: 8px;
        color: {ui['border_color']};
        font-size: 1.2rem;
        opacity: 0;
        pointer-events: none;
        animation: cave-sparkle 780ms ease-out 100ms both;
    }}
    @keyframes cave-pop {{
        from {{ opacity: 0; transform: translateY(8px) scale(0.985); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    @keyframes cave-glow {{
        0% {{ box-shadow: 0 0 0 rgba(197, 138, 69, 0); }}
        35% {{ box-shadow: 0 0 22px rgba(197, 138, 69, 0.24); }}
        100% {{ box-shadow: 0 5px 16px rgba(38, 58, 53, 0.16); }}
    }}
    @keyframes cave-sparkle {{
        0% {{ opacity: 0; transform: translateY(8px) scale(0.5) rotate(-25deg); }}
        35% {{ opacity: 0.8; }}
        100% {{ opacity: 0; transform: translateY(-12px) scale(1.15) rotate(25deg); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
        }}
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
        background-color: #314B43;
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
    .stApp:has(.game-header) [data-testid="stAppViewContainer"] .main .block-container {{
        position: fixed;
        z-index: 1000;
        inset: 2vh 2vw;
        width: auto;
        max-width: none;
        height: 96vh;
        overflow-y: auto;
        padding: 1.2rem clamp(1rem, 3vw, 2.5rem) 2rem;
        border: 1px solid var(--line);
        border-radius: 22px;
        background: var(--paper);
        box-shadow: 0 20px 60px rgba(38, 58, 53, 0.24);
    }}
    .stApp:has(.game-header) [data-testid="stSidebar"],
    .stApp:has(.game-header) [data-testid="stHeader"] {{
        display: none;
    }}
    .st-key-game-toolbar {{
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: linear-gradient(110deg, var(--hero-start), var(--paper));
    }}
    .st-key-game-toolbar .stButton button {{
        min-height: 3rem;
        padding: 0.45rem 0.55rem;
        font-size: 0.9rem;
        line-height: 1.15;
    }}
    .st-key-game-navigation {{
        padding: 0.65rem 0.85rem 0.15rem;
        margin: 0.2rem 0 1rem;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--paper);
    }}
    .st-key-game-navigation .stButton button {{
        min-height: 2.65rem;
        padding: 0.4rem 0.6rem;
        font-size: 0.9rem;
        line-height: 1.1;
    }}
    [data-testid="stDialog"]:has(.crafting-modal-marker) {{
        width: 96vw !important;
        max-width: 96vw !important;
        height: 94vh !important;
        max-height: 94vh !important;
        overflow-y: auto !important;
    }}
    .crafting-modal-marker {{
        display: none;
    }}
    @media (max-width: 700px) {{
        .stApp:has(.game-header) [data-testid="stAppViewContainer"] .main .block-container {{
            inset: 0;
            width: 100vw;
            height: 100vh;
            border-radius: 0;
            padding: 0.75rem 0.65rem 1rem;
        }}
        .st-key-game-toolbar .stButton button,
        .st-key-game-navigation .stButton button {{
            min-height: 2.5rem;
            padding: 0.3rem 0.35rem;
            font-size: 0.75rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

def pixel_icon_html(icon, label="", size=32):
    return render_pixel_icon_html(icon, label, size, art_style)

def icon_text(icon, label, size=26):
    return render_icon_text(icon, label, size, art_style)

def paper_drawing_html(icon, label, size=94):
    return render_paper_drawing_html(icon, label, size, art_style)

def pixel_button(label, icon, key, **kwargs):
    widget_key = safe_widget_key(key)
    st.markdown(
        render_icon_button_style(icon, widget_key, art_style),
        unsafe_allow_html=True,
    )
    return st.button(label, key=widget_key, **kwargs)

# Keyboard shortcut bridge
with st.container(key="admin-hotkey"):
    if st.button("Open Admin Panel", key="admin_hotkey_button"):
        st.session_state.state = "ADMIN"
        st.session_state.show_actions = False
        st.session_state.show_inventory_modal = False
        st.rerun()

components.html("""
<script>
    const appDocument = window.parent.document;
    if (!appDocument.__cavemanTycoonAdminShortcut) {
        appDocument.__cavemanTycoonAdminShortcut = true;
        appDocument.addEventListener("keydown", (event) => {
            const activeElement = appDocument.activeElement;
            if (
                event.key.toLowerCase() !== "q" ||
                event.repeat ||
                event.altKey ||
                event.ctrlKey ||
                event.metaKey ||
                activeElement?.matches("input, textarea, select, [contenteditable='true'], [role='textbox']") ||
                activeElement?.isContentEditable
            ) {
                return;
            }

            const adminButton = Array.from(appDocument.querySelectorAll("button"))
                .find((button) => button.textContent.trim() === "Open Admin Panel");
            if (adminButton) {
                event.preventDefault();
                adminButton.click();
            }
        });
    }
</script>
""", height=0)

def set_notification(text):
    st.session_state.message = text
    st.session_state.message_expiry = time.time() + 2.5

def inventory_load(inventory):
    return sum(max(0, count) for count in inventory.values())

def render_storage_inventory(
    title,
    inventory,
    destination,
    items,
    source_capacity,
    destination_capacity,
    transfer_label,
    key_prefix,
):
    title_icon = "🎒" if title == "Backpack" else "🧺"
    st.markdown(
        f"#### {icon_text(title_icon, title)}",
        unsafe_allow_html=True,
    )
    st.caption(f"{inventory_load(inventory)}/{source_capacity} items")
    if not items:
        st.info("No items in this category.")
        return

    destination_space = max(
        0, destination_capacity - inventory_load(destination)
    )
    item_columns = st.columns(min(4, len(items)))
    for index, item in enumerate(items):
        source_count = max(0, inventory.get(item, 0))
        transfer_count = min(source_count, destination_space)
        item_data = ITEM_ENCYCLOPEDIA.get(item, {})
        icon = item_data.get("icon", "📦")
        with item_columns[index % len(item_columns)]:
            with st.container(border=True):
                st.markdown(
                    pixel_icon_html(icon, item, 38),
                    unsafe_allow_html=True,
                )
                st.markdown(f"**{item}**")
                st.caption(f"{source_count} owned")
                if pixel_button(
                    f"{transfer_label} {transfer_count}",
                    icon,
                    key=f"{key_prefix}_{item}",
                    disabled=transfer_count == 0,
                ):
                    inventory[item] = source_count - transfer_count
                    destination[item] = destination.get(item, 0) + transfer_count
                    st.rerun()

def maybe_trigger_mouse_raid():
    if st.session_state.mice_raid_pending:
        return
    repellent_level = st.session_state.mouse_repellent_level
    raid_chance = max(0.0, 0.30 - 0.10 * repellent_level)
    if random.random() < raid_chance:
        st.session_state.mice_raid_pending = True
        st.session_state.mice_raid_deadline = time.time() + 12

def resolve_mouse_raid():
    st.session_state.mice_raid_pending = False
    candidates = None
    storage_load = inventory_load(st.session_state.storage)
    backpack_load = inventory_load(st.session_state.inventory)
    insulation_level = st.session_state.mouse_insulation_level

    if (
        storage_load
        and insulation_level < 3
        and random.random() < (3 - insulation_level) / 3
    ):
        candidates = st.session_state.storage
    elif backpack_load:
        candidates = st.session_state.inventory
    elif storage_load and insulation_level < 3:
        candidates = st.session_state.storage

    stolen_items = (
        [name for name, count in candidates.items() if count > 0]
        if candidates is not None
        else []
    )
    if stolen_items:
        stolen_item = random.choice(stolen_items)
        candidates[stolen_item] -= 1
        set_notification(f"The mice stole 1 {stolen_item}!")
    else:
        set_notification("The mice found nothing to steal.")

@st.fragment(run_every="1s")
def render_mouse_raid():
    if not st.session_state.mice_raid_pending:
        return

    remaining_seconds = max(
        0, int(st.session_state.mice_raid_deadline - time.time() + 0.999)
    )
    if remaining_seconds == 0:
        resolve_mouse_raid()
        st.warning(st.session_state.message)
        return

    st.warning("Mice are raiding! Click quickly to scare them off before they steal an item.")
    if pixel_button("Scare off the mice", "🖱️", "scare_mice"):
        if (
            st.session_state.mice_raid_pending
            and time.time() < st.session_state.mice_raid_deadline
        ):
            st.session_state.mice_raid_pending = False
            set_notification("You scared the mice away!")
            st.success("You scared the mice away!")
            return
    st.caption(f"They'll grab something in {remaining_seconds} seconds.")

def purchase_storage_upgrade(upgrade):
    level_key = f"mouse_{upgrade}_level"
    level = st.session_state[level_key]
    if level >= 3:
        return
    costs = (
        {"Dirt": 5 * (level + 1), "Roots": 4 * (level + 1)}
        if upgrade == "insulation"
        else {"Dead Flower": level + 1, "Roots": 3 * (level + 1)}
    )
    if not all(st.session_state.inventory.get(item, 0) >= amount for item, amount in costs.items()):
        return
    for item, amount in costs.items():
        st.session_state.inventory[item] -= amount
    st.session_state[level_key] += 1
    upgrade_label = "Insulation" if upgrade == "insulation" else "Mouse repellent"
    set_notification(f"{upgrade_label} upgraded to level {level + 1}!")

def craft_tree_tier(branch, track):
    return max(
        (
            item_data["tier"]
            for item_name, item_data in CRAFT_TREE_ITEMS.items()
            if item_data["branch"] == branch
            and item_data["track"] == track
            and st.session_state.inventory.get(item_name, 0) > 0
        ),
        default=0,
    )

def branch_unlocked(branch):
    paper_name = CRAFT_TREE_BRANCHES[branch]["paper"]
    unlocked = st.session_state.unlocked_craft_branches
    has_existing_progress = any(
        st.session_state.inventory.get(item_name, 0) > 0
        for item_name, item_data in CRAFT_TREE_ITEMS.items()
        if item_data["branch"] == branch
    )
    if (
        st.session_state.inventory.get(paper_name, 0) > 0
        or has_existing_progress
    ) and branch not in unlocked:
        unlocked.append(branch)
    return branch in unlocked

def perform_branch_action(branch):
    if not branch_unlocked(branch):
        return
    branch_data = CRAFT_TREE_BRANCHES[branch]
    tool_tier = craft_tree_tier(branch, "tools")
    upgrade_tier = craft_tree_tier(branch, "upgrades")
    amount = 1 + tool_tier + upgrade_tier
    reward_pool = branch_data["rewards"][:min(len(branch_data["rewards"]), 2 + tool_tier + upgrade_tier)]
    item = random.choice(reward_pool)
    current_load = inventory_load(st.session_state.inventory)
    amount = min(amount, max(0, BACKPACK_CAPACITY - current_load))
    if amount == 0:
        set_notification("Your backpack is full. Store items at camp before gathering more.")
        return
    st.session_state.inventory[item] = st.session_state.inventory.get(item, 0) + amount
    icon = ITEM_ENCYCLOPEDIA[item]["icon"]
    set_notification(
        f"+{amount} {icon} {item} while {branch_data['action'].lower()}ing!"
    )
    maybe_trigger_mouse_raid()

def perform_dig():
    tool_mult = st.session_state.tool_boosters.get("Pebble Axe", {}).get("multiplier", 2) if st.session_state.inventory.get("Pebble Axe", 0) > 0 else 1
    undiscovered_papers = [
        branch_data["paper"]
        for branch, branch_data in CRAFT_TREE_BRANCHES.items()
        if not branch_unlocked(branch)
    ]
    if undiscovered_papers and random.random() < 0.07:
        item = random.choice(undiscovered_papers)
        amount = 1
        branch = next(
            name
            for name, branch_data in CRAFT_TREE_BRANCHES.items()
            if branch_data["paper"] == item
        )
        st.session_state.unlocked_craft_branches.append(branch)
    else:
        roll = random.random()
        if roll < 0.40:
            item = random.choice(["Dirt", "Worms", "Roots"])
        elif roll < 0.65:
            item = random.choice(["Pebbles", "Coal"])
        elif roll < 0.85:
            item = random.choice(["Soil", "Old Carrots", "Dead Flower"])
        else:
            item = random.choice(["Fresh Carrots", "Roses", "Perfect Soil", "Metal Fragments"])
        amount = None
        
    current_load = inventory_load(st.session_state.inventory)
    if amount is None:
        amount = min(tool_mult, max(0, BACKPACK_CAPACITY - current_load))
    else:
        amount = min(amount, max(0, BACKPACK_CAPACITY - current_load))
    if amount == 0:
        set_notification("Your backpack is full. Store items at camp before gathering more.")
        return
    st.session_state.inventory[item] += amount
    meta = ITEM_ENCYCLOPEDIA.get(item, {"icon": "📦"})
    icon = meta["icon"]
    
    if item in undiscovered_papers:
        set_notification(f"Found an illustrated plan: {item}. A new crafting section is revealed!")
    elif amount < tool_mult:
        set_notification(f"Backpack nearly full: collected {amount} {icon} {item}.")
    elif tool_mult > 1:
        set_notification(f"+{tool_mult}x {icon} {item} (Tool Boost!)")
    else:
        set_notification(f"+1 {icon} {item}")
    maybe_trigger_mouse_raid()

if (
    st.session_state.mice_raid_pending
    and time.time() >= st.session_state.mice_raid_deadline
):
    resolve_mouse_raid()


@st.dialog("Recipe Book & Crafting", width="large")
def crafting_modal():
    st.markdown("<div class='crafting-modal-marker'></div>", unsafe_allow_html=True)
    st.markdown(f"### {icon_text('📜', 'Recipe Book & Crafting')}", unsafe_allow_html=True)

    has_perfect_soil = st.session_state.inventory.get("Perfect Soil", 0) > 0
    has_crafted_fine_dirt = st.session_state.inventory.get("Fine dirt", 0) > 0
    fine_dirt_unlocked = has_perfect_soil or has_crafted_fine_dirt
    has_found_pebbles = st.session_state.inventory.get("Pebbles", 0) > 0
    has_crafted_pebble_axe = st.session_state.inventory.get("Pebble Axe", 0) > 0
    pebble_axe_unlocked = has_found_pebbles or has_crafted_pebble_axe
    has_stone_oven = st.session_state.inventory.get("Stone Oven", 0) > 0

    for recipe_name, recipe_data in st.session_state.recipes.items():
        tree_item = CRAFT_TREE_ITEMS.get(recipe_name)
        if tree_item:
            branch = tree_item["branch"]
            track = tree_item["track"]
            if not branch_unlocked(branch):
                continue
            tier = tree_item["tier"]
            if tier != craft_tree_tier(branch, track) + 1:
                continue
            if track == "upgrades" and craft_tree_tier(branch, "tools") < tier:
                continue
        if recipe_name == "Fine dirt" and not fine_dirt_unlocked:
            continue
        if recipe_name == "Pebble Axe" and not pebble_axe_unlocked:
            continue
        if recipe_name == "Molten Metal" and not has_stone_oven:
            continue

        tooltip_lines = []
        if "alternatives" in recipe_data:
            for alternative in recipe_data["alternatives"]:
                parts = []
                for ingredient, required in alternative.items():
                    owned = st.session_state.inventory.get(ingredient, 0)
                    availability = "Ready" if owned >= required else "Missing"
                    parts.append(
                        f"{availability}: {required}x {ingredient} (Have: {owned})"
                    )
                tooltip_lines.append(" or ".join(parts))
        else:
            for ingredient, required in recipe_data.items():
                owned = st.session_state.inventory.get(ingredient, 0)
                availability = "Ready" if owned >= required else "Missing"
                tooltip_lines.append(
                    f"{availability}: {required}x {ingredient} (Have: {owned})"
                )

        st.markdown(f"""
            <div class="recipe-tooltip">
                <h4 style="margin-bottom: 2px;">{icon_text('🧪', recipe_name)}</h4>
                <div class="tooltip-text"><b>Recipe Requirements:</b><br>{"<br>".join(tooltip_lines)}</div>
            </div>
        """, unsafe_allow_html=True)

        chosen_option = None
        if "alternatives" in recipe_data:
            for alternative in recipe_data["alternatives"]:
                if all(
                    st.session_state.inventory.get(ingredient, 0) >= required
                    for ingredient, required in alternative.items()
                ):
                    chosen_option = alternative
        elif all(
            st.session_state.inventory.get(ingredient, 0) >= required
            for ingredient, required in recipe_data.items()
        ):
            chosen_option = recipe_data

        craft_blocked_by_capacity = False
        can_craft = chosen_option is not None
        if can_craft:
            ingredients_used = sum(chosen_option.values())
            projected_load = inventory_load(st.session_state.inventory) - ingredients_used + 1
            if projected_load > BACKPACK_CAPACITY:
                can_craft = False
                craft_blocked_by_capacity = True

        if can_craft:
            recipe_icon = ITEM_ENCYCLOPEDIA.get(recipe_name, {}).get("icon", "🧱")
            if pixel_button(
                f"Craft {recipe_name}",
                recipe_icon,
                key=f"craft_btn_{recipe_name}",
            ):
                for ingredient, required in chosen_option.items():
                    st.session_state.inventory[ingredient] -= required
                st.session_state.inventory[recipe_name] = (
                    st.session_state.inventory.get(recipe_name, 0) + 1
                )
                meta = ITEM_ENCYCLOPEDIA.get(recipe_name, {"icon": "📦"})
                set_notification(f"Crafted {meta['icon']} {recipe_name}!")
                st.rerun()
        elif craft_blocked_by_capacity:
            st.markdown(
                "<span style='color: #9B2C2C; font-weight: bold;'>Backpack full — store items before crafting.</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<span style='color: #9B2C2C; font-weight: bold;'>Missing ingredients.</span>",
                unsafe_allow_html=True,
            )
        st.markdown("---")


# Router
if st.session_state.state == "MENU":
    st.markdown("""
        <div class="menu-hero">
            <div class="menu-mark">""" + pixel_icon_html("🦴", "Caveman Tycoon", 64) + """</div>
            <h1>Caveman Tycoon</h1>
            <p>Start with the basics. Gather, craft, and build your way forward.</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if pixel_button("Play Now", "🚀", "menu_play"):
            st.session_state.state = "TUTORIAL"
            st.rerun()
        if pixel_button("Interface Settings", "⚙️", "menu_settings"):
            st.session_state.state = "SETTINGS"
            st.rerun()
        if pixel_button("Audio", "🔊", "menu_audio"):
            st.session_state.state = "AUDIO"
            st.rerun()
        if pixel_button("Performance", "⚡", "menu_performance"):
            st.session_state.state = "PERFORMANCE"
            st.rerun()
        if pixel_button("Credits", "🎉", "menu_credits"):
            st.session_state.state = "CREDITS"
            st.rerun()

elif st.session_state.state == "SETTINGS":
    st.markdown("""
        <div class="page-hero">
            <h1>""" + icon_text("⚙️", "Interface & Material Colors", 38) + """</h1>
            <p>Personalize notification highlights and the colors used for your item cards.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    setting_columns = st.columns(2)
    with setting_columns[0]:
        ui["theme"] = st.selectbox(
            "Color theme",
            list(visual_themes),
            index=list(visual_themes).index(ui["theme"]),
        )
    with setting_columns[1]:
        art_styles = ["Advanced Simple", "Pixel Art", "Soft Illustrated"]
        ui["art_style"] = st.selectbox(
            "Art style",
            art_styles,
            index=art_styles.index(ui["art_style"]),
        )
    st.caption(
        "Themes recolor the interface; art styles change item and navigation illustrations."
    )

    with st.expander("Notification and item card colors"):
        st.session_state.ui_settings["bg_color"] = st.color_picker("Notification Highlight Background Color", st.session_state.ui_settings["bg_color"])
        st.session_state.ui_settings["text_color"] = st.color_picker("Notification Text Color", st.session_state.ui_settings["text_color"])
        st.session_state.ui_settings["border_color"] = st.color_picker("Notification Border Color", st.session_state.ui_settings["border_color"])

        st.markdown(f"### {icon_text('🎨', 'Individual Material Card Colors')}", unsafe_allow_html=True)
        for item_name in ITEM_ENCYCLOPEDIA:
            curr_color = st.session_state.item_custom_colors.get(item_name, "#F0F0F0")
            st.session_state.item_custom_colors[item_name] = st.color_picker(f"Background color for {item_name}", curr_color, key=f"color_picker_{item_name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Menu"):
        st.session_state.state = "MENU"
        st.rerun()

elif st.session_state.state == "TUTORIAL":
    st.markdown("""
        <div class="page-hero">
            <h1>""" + icon_text("🦴", "Welcome to Caveman Tycoon", 38) + """</h1>
            <p>A small guide to getting started in your new underground home.</p>
        </div>
    """, unsafe_allow_html=True)
    guide_col1, guide_col2 = st.columns(2)
    with guide_col1:
        st.markdown(f"### {icon_text('⛏️', 'Gather')}", unsafe_allow_html=True)
        st.write("Open **Actions** in the cave and dig to find materials, food, and rare discoveries.")
    with guide_col2:
        st.markdown(f"### {icon_text('🧪', 'Craft')}", unsafe_allow_html=True)
        st.write("Check the recipe book in the sidebar. Gather the listed ingredients to craft available items.")
    st.info("Your backpack holds 200 items. Dig to uncover illustrated plans that reveal new crafting paths. Build storage at camp, and press **Q** to open the Admin Panel.")
    if pixel_button("Start Playing!", "🚀", "tutorial_start"):
        st.session_state.state = "PLAYING"
        st.rerun()

elif st.session_state.state == "CREDITS":
    st.markdown("""
        <div class="page-hero">
            <h1>""" + icon_text("🎉", "Thanks for playing", 38) + """</h1>
            <p>Caveman Tycoon is made by Kai. We hope you enjoy your time underground.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("← Back to Menu"):
        st.session_state.state = "MENU"
        st.rerun()

elif st.session_state.state == "ADMIN":
    st.markdown("""
        <div class="page-hero">
            <h1>""" + icon_text("🛠️", "Advanced Admin Panel", 38) + """</h1>
            <p>Manage your resources, recipes, and tool settings.</p>
        </div>
    """, unsafe_allow_html=True)
    admin_summary = st.columns(3)
    admin_summary[0].metric("Inventory entries", len(st.session_state.inventory))
    admin_summary[1].metric(
        "Discovered items",
        sum(amount > 0 for amount in st.session_state.inventory.values()),
    )
    admin_summary[2].metric("Registered recipes", len(st.session_state.recipes))

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        with st.container(key="admin-unlock-card"):
            st.markdown(f"#### {icon_text('🌿', 'Unlock collection')}", unsafe_allow_html=True)
            st.caption("Discover every item and open all crafting paths.")
            if pixel_button("Unlock All Items & Crafting Tree", "✨", "unlock_all"):
                for item in st.session_state.inventory:
                    amount = max(st.session_state.inventory[item], 1)
                    st.session_state.inventory[item] = amount
                    st.session_state[f"admin_give_{item}"] = amount
                st.success("Unlocked all items and trees!")
                st.rerun()
    with col_g2:
        with st.container(key="admin-unlimited-card"):
            st.markdown(f"#### {icon_text('♾️', 'Unlimited supplies')}", unsafe_allow_html=True)
            st.caption("Set every inventory quantity to 999.")
            if pixel_button("Enable Unlimited Resources (999x All)", "♾️", "unlimited_resources"):
                for item in st.session_state.inventory:
                    st.session_state.inventory[item] = 999
                    st.session_state[f"admin_give_{item}"] = 999
                st.success("Set all resources to 999!")
                st.rerun()

    admin_tab_icons = st.columns(3)
    for column, (icon, label) in zip(
        admin_tab_icons,
        [
            ("📦", "Inventory"),
            ("⚡", "Boosters"),
            ("🧪", "Recipes"),
        ],
    ):
        with column:
            st.markdown(icon_text(icon, label), unsafe_allow_html=True)
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(
        ["Give Items & Inventory", "Tool Boosters (Lv. 1-100)", "Custom Recipes"]
    )

    with admin_tab1:
        st.markdown(
            "<div class='admin-tab-intro admin-inventory-intro'>Search or choose a group, then edit item quantities.</div>",
            unsafe_allow_html=True,
        )
        inventory_groups = {}
        for item_name in st.session_state.inventory:
            tree_item = CRAFT_TREE_ITEMS.get(item_name)
            if tree_item:
                group = f"{tree_item['branch']} {tree_item['track'].title()}"
            else:
                category = ITEM_ENCYCLOPEDIA.get(item_name, {}).get("category", "other")
                group = category.replace("_", " ").title()
            inventory_groups.setdefault(group, []).append(item_name)

        group_names = sorted(inventory_groups)
        filter_col, search_col = st.columns([1, 2])
        with filter_col:
            selected_group = st.selectbox(
                "Item group",
                ["All groups", *group_names],
                key="admin_inventory_group",
            )
        with search_col:
            item_search = st.text_input(
                "Search items",
                placeholder="Type an item name...",
                key="admin_inventory_search",
            ).strip().casefold()

        shown_groups = (
            group_names if selected_group == "All groups" else [selected_group]
        )
        matching_count = 0
        filtered_groups = {}
        for group in shown_groups:
            names = [
                name
                for name in inventory_groups[group]
                if item_search in name.casefold()
            ]
            if names:
                filtered_groups[group] = names
                matching_count += len(names)
        st.caption(f"{matching_count} item(s) match the current filters.")

        for group, item_names in filtered_groups.items():
            with st.expander(f"{group} · {len(item_names)} items"):
                for start in range(0, len(item_names), 3):
                    quantity_columns = st.columns(3)
                    for column, item in zip(
                        quantity_columns, item_names[start:start + 3]
                    ):
                        with column:
                            widget_key = f"admin_give_{item}"
                            if widget_key not in st.session_state:
                                st.session_state[widget_key] = int(
                                    st.session_state.inventory[item]
                                )
                            st.session_state.inventory[item] = st.number_input(
                                item,
                                min_value=0,
                                key=widget_key,
                            )

    with admin_tab2:
        st.markdown(
            "<div class='admin-tab-intro admin-booster-intro'>Adjust tool levels and immediately see their gathering multipliers.</div>",
            unsafe_allow_html=True,
        )
        for tool_name in ["Pebble Axe", "Stone Oven"]:
            if tool_name not in st.session_state.tool_boosters:
                st.session_state.tool_boosters[tool_name] = {"level": 1, "multiplier": 2}
            
            with st.container(border=True):
                tool_icon = ITEM_ENCYCLOPEDIA.get(tool_name, {}).get("icon", "🛠️")
                st.markdown(
                    f"#### {icon_text(tool_icon, tool_name)}",
                    unsafe_allow_html=True,
                )
                curr_lvl = st.session_state.tool_boosters[tool_name]["level"]
                new_lvl = st.slider(f"Level for {tool_name}", 1, 100, value=curr_lvl, key=f"slider_lvl_{tool_name}")
                calculated_mult = new_lvl * 2
                st.session_state.tool_boosters[tool_name]["level"] = new_lvl
                st.session_state.tool_boosters[tool_name]["multiplier"] = calculated_mult
                st.metric("Current Efficiency Multiplier", f"x{calculated_mult}")

    with admin_tab3:
        st.markdown(
            "<div class='admin-tab-intro admin-recipe-intro'>Register a custom crafted item with a recipe and a clear in-game purpose.</div>",
            unsafe_allow_html=True,
        )
        with st.form("custom_recipe_form"):
            new_recipe_name = st.text_input("New Recipe / Item Name")
            recipe_meta_col, recipe_icon_col = st.columns(2)
            with recipe_meta_col:
                new_item_rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Crafted"])
            with recipe_icon_col:
                selected_icon = st.selectbox(
                    "Pixel art icon",
                    list(PIXEL_ICON_CHOICES),
                )
                new_item_icon = PIXEL_ICON_CHOICES[selected_icon]
            desc_col, use_col = st.columns(2)
            with desc_col:
                new_item_desc = st.text_area("Description")
            with use_col:
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
    st.markdown("""
        <div class="page-hero">
            <h1>""" + icon_text("🔊", "Audio Settings", 38) + """</h1>
            <p>Audio controls are not available yet.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Back"):
        st.session_state.state = "MENU"
        st.rerun()

elif st.session_state.state == "PERFORMANCE":
    st.markdown("""
        <div class="page-hero">
            <h1>""" + icon_text("⚙️", "Performance", 38) + """</h1>
            <p>Performance options are not available yet.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Back"):
        st.session_state.state = "MENU"
        st.rerun()

elif st.session_state.state == "PLAYING":
    with st.container(key="game-toolbar"):
        col_title, col_inventory, col_crafting, col_menu = st.columns(
            [3, 1.35, 1.05, 0.75], vertical_alignment="center"
        )
        with col_title:
            st.markdown("""
                <div class="game-header">
                    <h2>""" + icon_text("🦴", "Caveman Tycoon", 32) + """</h2>
                    <p>Gather resources, discover new materials, and craft what you need.</p>
                </div>
            """, unsafe_allow_html=True)
        with col_inventory:
            if pixel_button("Open Inventory", "🎒", "open_inventory"):
                st.session_state.show_inventory_modal = False
                inventory_modal()
        with col_crafting:
            if pixel_button("Crafting", "📜", "open_crafting"):
                st.session_state.show_inventory_modal = False
                crafting_modal()
        with col_menu:
            if pixel_button("Menu", "🏠", "game_menu"):
                st.session_state.state = "MENU"
                st.session_state.show_actions = False
                st.session_state.show_inventory_modal = False
                st.rerun()

    with st.container(key="game-navigation"):
        group_icons = {
            "Explore": "⛏️",
            "Collection": "📖",
            "Settlement": "🏕️",
        }
        group_columns = st.columns(len(game_groups))
        for column, group_name in zip(group_columns, game_groups):
            with column:
                group_key = f"game_group_{group_name.lower()}"
                st.markdown(
                    render_icon_button_style(
                        group_icons[group_name], group_key, art_style
                    ),
                    unsafe_allow_html=True,
                )
                if st.button(
                    group_name,
                    key=group_key,
                    type=(
                        "primary"
                        if st.session_state.game_group == group_name
                        else "secondary"
                    ),
                ):
                    st.session_state.game_group = group_name
                    if st.session_state.game_page not in game_groups[group_name]:
                        st.session_state.game_page = game_groups[group_name][0]
                    st.rerun()

        page_icons = {
            "Cave": ("⛏️", "cave"),
            "Craft Tree": ("🌳", "craft_tree"),
            "Items Book": ("📖", "items_book"),
            "Camp": ("🏕️", "camp"),
        }
        game_pages = game_groups[st.session_state.game_group]
        page_columns = st.columns(len(game_pages))
        for column, page_name in zip(page_columns, game_pages):
            page_icon, page_id = page_icons[page_name]
            with column:
                page_key = f"game_page_{page_id}"
                st.markdown(
                    render_icon_button_style(page_icon, page_key, art_style),
                    unsafe_allow_html=True,
                )
                if st.button(
                    page_name,
                    key=page_key,
                    type=(
                        "primary"
                        if st.session_state.game_page == page_name
                        else "secondary"
                    ),
                ):
                    st.session_state.game_page = page_name
                    st.rerun()

        current_page_icon = {
            page_name: page_icons[page_name][0]
            for page_name in game_pages
        }[st.session_state.game_page]
        st.markdown(
            f"<div class='game-page-heading'>{icon_text(current_page_icon, st.session_state.game_page)}"
            f"<span>{st.session_state.game_group.upper()} · "
            f"PAGE {game_pages.index(st.session_state.game_page) + 1} "
            f"OF {len(game_pages)}</span></div>",
            unsafe_allow_html=True,
        )

    render_mouse_raid()

    st.markdown("---")
    backpack_load = inventory_load(st.session_state.inventory)
    st.markdown(
        f"{icon_text('🎒', f'Backpack: {backpack_load}/{BACKPACK_CAPACITY} items', 20)}",
        unsafe_allow_html=True,
    )

    col_main = st.columns(1)[0]
    with col_main:
        if st.session_state.selected_item:
            sel = st.session_state.selected_item
            info = ITEM_ENCYCLOPEDIA.get(sel, {})
            selected_columns = st.columns([0.08, 1])
            with selected_columns[0]:
                st.markdown(
                    pixel_icon_html(info.get("icon", "📦"), sel, 32),
                    unsafe_allow_html=True,
                )
            with selected_columns[1]:
                st.info(
                    f"Selected item: {sel} "
                    f"(Owned: {st.session_state.inventory.get(sel, 0)}) — "
                    f"{info.get('use', '')}"
                )

        if st.session_state.game_page == "Cave":
            st.markdown("""
                <div class="cave-panel">
                    <h3>""" + icon_text("⛏️", "The Great Cave") + """</h3>
                    <p>Every expedition starts with a single dig.</p>
                </div>
            """, unsafe_allow_html=True)
            
            if pixel_button("Actions", "⛏️", "actions_btn"):
                st.session_state.show_actions = not st.session_state.show_actions
                st.session_state.show_inventory_modal = False
                st.rerun()
            
            if st.session_state.show_actions:
                st.markdown("### Choose Action:")

                available_actions = [("Dig", None, "⛏️")]
                available_actions.extend(
                    (branch_data["action"], branch, branch_data["icon"])
                    for branch, branch_data in CRAFT_TREE_BRANCHES.items()
                    if branch_unlocked(branch)
                    and craft_tree_tier(branch, "tools") > 0
                )
                action_columns = st.columns([1] * len(available_actions) + [2])
                for column, (label, branch, action_icon) in zip(
                    action_columns, available_actions
                ):
                    with column:
                        action_key = f"action_{branch or 'dig'}"
                        if pixel_button(label, action_icon, action_key):
                            if branch is None:
                                perform_dig()
                            else:
                                perform_branch_action(branch)
                            st.session_state.show_inventory_modal = False
                            st.rerun()
                with action_columns[-1]:
                    if st.session_state.message and time.time() < st.session_state.message_expiry:
                        st.markdown(
                            f"<div class='dig-popup'>{replace_icons(st.session_state.message)}</div>",
                            unsafe_allow_html=True,
                        )

        if st.session_state.game_page == "Craft Tree":
            st.markdown("""
                <div class="craft-tree-hero">
                    <h3>""" + icon_text("🌳", "The Crafting Frontier") + """</h3>
                    <p>Craft tools to unlock gathering actions, then build upgrades to increase their yields.</p>
                    <span class="craft-tree-stat">60 CRAFTABLE ITEMS</span>
                    <span class="craft-tree-stat">3 GATHERING DISCIPLINES</span>
                    <span class="craft-tree-stat">10 TIERS PER PATH</span>
                </div>
            """, unsafe_allow_html=True)

            unlocked_branches = [
                (branch, branch_data)
                for branch, branch_data in CRAFT_TREE_BRANCHES.items()
                if branch_unlocked(branch)
            ]
            locked_branches = [
                (branch, branch_data)
                for branch, branch_data in CRAFT_TREE_BRANCHES.items()
                if not branch_unlocked(branch)
            ]
            if locked_branches:
                st.markdown("#### Discover illustrated plans")
                st.caption(
                    "Crafting paths stay hidden until you find their illustrated plans while digging."
                )
                paper_columns = st.columns(min(3, len(locked_branches)))
                for index, (branch, branch_data) in enumerate(locked_branches):
                    paper = CRAFT_TREE_PAPERS[branch]
                    with paper_columns[index % len(paper_columns)]:
                        with st.container(border=True):
                            st.markdown(
                                paper_drawing_html(
                                    branch_data["icon"], paper["name"], 88
                                ),
                                unsafe_allow_html=True,
                            )
                            st.markdown(f"**{paper['name']}**")
                            st.caption(paper["description"])
                            st.caption("Undiscovered · find it while digging")

            if not unlocked_branches:
                st.info(
                    "No crafting paths revealed yet. Explore the cave to find a paper sketch."
                )
            else:
                st.markdown(
                    f"{icon_text('🛠️', 'Tools')} &nbsp;&nbsp; "
                    f"{icon_text('⬆️', 'Upgrades')}",
                    unsafe_allow_html=True,
                )
                tools_tab, upgrades_tab = st.tabs(["Tools", "Upgrades"])
                for track, category_tab in zip(
                    ("tools", "upgrades"), (tools_tab, upgrades_tab)
                ):
                    with category_tab:
                        branch_icon_columns = st.columns(len(unlocked_branches))
                        for column, (branch_name, branch_info) in zip(
                            branch_icon_columns, unlocked_branches
                        ):
                            with column:
                                st.markdown(
                                    paper_drawing_html(
                                        branch_info["icon"], branch_name, 56
                                    ),
                                    unsafe_allow_html=True,
                                )
                        branch_tabs = st.tabs(
                            [branch for branch, _ in unlocked_branches]
                        )
                        for (branch, branch_data), branch_tab in zip(
                            unlocked_branches, branch_tabs
                        ):
                            with branch_tab:
                                current_tier = craft_tree_tier(branch, track)
                                item_names = [
                                    item_name
                                    for item_name, item_data in CRAFT_TREE_ITEMS.items()
                                    if item_data["branch"] == branch
                                    and item_data["track"] == track
                                ]
                                st.progress(
                                    current_tier / len(item_names),
                                    text=(
                                        f"{branch} {track.title()} · "
                                        f"Tier {current_tier}/{len(item_names)}"
                                    ),
                                )
                                if track == "upgrades":
                                    st.caption(
                                        f"Tool tier {craft_tree_tier(branch, 'tools')} "
                                        "unlocks the maximum upgrade tier you can craft."
                                    )

                                for tier, item_name in enumerate(item_names, start=1):
                                    item_info = ITEM_ENCYCLOPEDIA[item_name]
                                    recipe = st.session_state.recipes[item_name]
                                    owned = st.session_state.inventory.get(item_name, 0)
                                    next_in_line = tier == current_tier + 1
                                    tier_unlocked = (
                                        track != "upgrades"
                                        or craft_tree_tier(branch, "tools") >= tier
                                    )
                                    can_afford = all(
                                        st.session_state.inventory.get(ingredient, 0)
                                        >= amount
                                        for ingredient, amount in recipe.items()
                                    )
                                    if owned > 0:
                                        status = f"Owned ×{owned}"
                                    elif tier <= current_tier:
                                        status = "Completed"
                                    elif next_in_line and tier_unlocked and can_afford:
                                        status = "Ready to craft"
                                    elif next_in_line and tier_unlocked:
                                        status = "Next tier"
                                    else:
                                        status = "Locked"

                                    with st.container(border=True):
                                        st.markdown(
                                            f"**Tier {tier}: {icon_text(item_info['icon'], item_name)}** · {status}",
                                            unsafe_allow_html=True,
                                        )
                                        st.caption(item_info["description"])
                                        st.write(f"**Purpose:** {item_info['use']}")
                                        if tier == 1 or (
                                            next_in_line and tier_unlocked
                                        ):
                                            requirements = ", ".join(
                                                f"{amount}× {ingredient}"
                                                for ingredient, amount in recipe.items()
                                            )
                                            recipe_label = (
                                                "First recipe"
                                                if tier == 1
                                                else "Next recipe"
                                            )
                                            st.caption(
                                                f"{recipe_label}: {requirements} · "
                                                "craft from the sidebar"
                                            )

        if st.session_state.game_page == "Items Book":
            discovered_items = sum(
                count > 0 for count in st.session_state.inventory.values()
            )
            st.markdown(f"""
                <div class="page-hero">
                    <h3>{icon_text('📖', 'Items Book')}</h3>
                    <p>Your discovery codex · {discovered_items} items found</p>
                </div>
            """, unsafe_allow_html=True)
            for item_name, info in ITEM_ENCYCLOPEDIA.items():
                if st.session_state.inventory.get(item_name, 0) > 0:
                    item_bg_color = st.session_state.item_custom_colors.get(item_name, info.get("color", "#F0F0F0"))
                    paper_branch = next(
                        (
                            branch
                            for branch, branch_data in CRAFT_TREE_BRANCHES.items()
                            if branch_data["paper"] == item_name
                        ),
                        None,
                    )
                    item_art = (
                        paper_drawing_html(
                            CRAFT_TREE_BRANCHES[paper_branch]["icon"],
                            item_name,
                            48,
                        )
                        if paper_branch
                        else pixel_icon_html(info.get("icon", "📦"), item_name, 32)
                    )
                    with st.expander(f"{item_name} ({info['rarity']})"):
                        st.markdown(f"""
                            <div style="background-color: {item_bg_color}; padding: 8px; border-radius: 6px; margin-bottom: 5px;">
                                {item_art}
                                <b>Owned:</b> {st.session_state.inventory.get(item_name, 0)}<br>
                                <b>Use:</b> {info['use']}
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    with st.container(border=True):
                        st.markdown(
                            f"<span class='item-shadow'>{pixel_icon_html(info.get('icon', '📦'), item_name, 24)} {item_name} ({info['rarity']}) — undiscovered</span>",
                            unsafe_allow_html=True,
                        )

        if st.session_state.game_page == "Camp":
            st.markdown(
                f"### {icon_text('🏕️', 'Camp Storage & Mouse Defense')}",
                unsafe_allow_html=True,
            )
            st.write("Build a safe place for supplies, then reinforce it against cave mice.")
            if not st.session_state.storage_built:
                storage_cost = {"Dirt": 8, "Roots": 5, "Pebbles": 5}
                st.info("Build a storage hut to hold 100 items separately from your backpack.")
                st.caption("Cost: " + " · ".join(
                    f"{amount} {item} (have {st.session_state.inventory.get(item, 0)})"
                    for item, amount in storage_cost.items()
                ))
                can_build_storage = all(
                    st.session_state.inventory.get(item, 0) >= amount
                    for item, amount in storage_cost.items()
                )
                if pixel_button(
                    "Build storage hut",
                    "🧺",
                    "build_storage_hut",
                    disabled=not can_build_storage,
                ):
                    for item, amount in storage_cost.items():
                        st.session_state.inventory[item] -= amount
                    st.session_state.storage_built = True
                    set_notification("Storage hut built! Your supplies are ready to move.")
                    st.rerun()
            else:
                storage_load = inventory_load(st.session_state.storage)
                st.metric("Storage", f"{storage_load}/{st.session_state.storage_capacity} items")
                available_categories = sorted({
                    ITEM_ENCYCLOPEDIA.get(item, {}).get("category", "other")
                    for item in set(st.session_state.inventory)
                    | set(st.session_state.storage)
                })
                category_order = [
                    "material", "food", "crafted", "tool",
                    "weapon", "fishing", "farming", "hunting",
                ]
                ordered_categories = [
                    category for category in category_order
                    if category in available_categories
                ] + [
                    category for category in available_categories
                    if category not in category_order
                ]
                if st.session_state.storage_category not in (
                    "all", *ordered_categories
                ):
                    st.session_state.storage_category = "all"

                category_icons = {
                    "material": "🪨", "food": "🍖", "crafted": "🧱",
                    "tool": "🛠️", "weapon": "⚔️", "fishing": "🎣",
                    "farming": "🌱", "hunting": "🏹", "other": "📦",
                }
                wheel_categories = ordered_categories[:8]
                wheel_categories += [None] * (8 - len(wheel_categories))
                wheel_rows = [
                    wheel_categories[:3],
                    [wheel_categories[7], "all", wheel_categories[3]],
                    [wheel_categories[6], wheel_categories[5], wheel_categories[4]],
                ]
                wheel_column, category_description = st.columns([1, 2])
                with wheel_column:
                    with st.container(key="storage-category-wheel"):
                        for row in wheel_rows:
                            wheel_columns = st.columns(3)
                            for column, category in zip(wheel_columns, row):
                                with column:
                                    if category is None:
                                        st.write("")
                                        continue
                                    if category == "all":
                                        label = "All"
                                        category_icon = "🗃️"
                                    else:
                                        label = category.title()
                                        category_icon = category_icons.get(category, "📦")
                                    if category == st.session_state.storage_category:
                                        label = f"Selected · {label}"
                                    if pixel_button(
                                        label,
                                        category_icon,
                                        key=f"storage_category_{category}",
                                        type=(
                                            "primary"
                                            if category == st.session_state.storage_category
                                            else "secondary"
                                        ),
                                    ):
                                        st.session_state.storage_category = category
                                        st.rerun()
                        for category in ordered_categories[8:]:
                            if pixel_button(
                                category.title(),
                                category_icons.get(category, "📦"),
                                key=f"storage_category_{category}",
                            ):
                                st.session_state.storage_category = category
                                st.rerun()

                with category_description:
                    selected_category = st.session_state.storage_category
                    selected_label = (
                        "All categories"
                        if selected_category == "all"
                        else selected_category.title()
                    )
                    st.markdown(f"#### {selected_label}")
                    st.caption("Choose a category from the wheel to filter both inventories.")
                    layout_button = (
                        "↕ Show inventories vertically"
                        if st.session_state.storage_horizontal
                        else "↔ Show inventories side by side"
                    )
                    if st.button(layout_button, key="toggle_storage_layout"):
                        st.session_state.storage_horizontal = (
                            not st.session_state.storage_horizontal
                        )
                        st.rerun()

                all_stored_items = sorted(
                    set(st.session_state.inventory) | set(st.session_state.storage)
                )
                stored_items = [
                    item for item in all_stored_items
                    if (
                        st.session_state.inventory.get(item, 0) > 0
                        or st.session_state.storage.get(item, 0) > 0
                    )
                    and (
                        st.session_state.storage_category == "all"
                        or ITEM_ENCYCLOPEDIA.get(item, {}).get(
                            "category", "other"
                        ) == st.session_state.storage_category
                    )
                ]
                if not any(
                    count > 0
                    for inventory in (
                        st.session_state.inventory, st.session_state.storage
                    )
                    for count in inventory.values()
                ):
                    st.info("Your backpack and storage are empty.")
                elif st.session_state.storage_horizontal:
                    backpack_column, storage_column = st.columns(2)
                    with backpack_column:
                        render_storage_inventory(
                            "Backpack",
                            st.session_state.inventory,
                            st.session_state.storage,
                            stored_items,
                            BACKPACK_CAPACITY,
                            st.session_state.storage_capacity,
                            "Store →",
                            "backpack",
                        )
                    with storage_column:
                        render_storage_inventory(
                            "Storage",
                            st.session_state.storage,
                            st.session_state.inventory,
                            stored_items,
                            st.session_state.storage_capacity,
                            BACKPACK_CAPACITY,
                            "Take ←",
                            "storage",
                        )
                else:
                    render_storage_inventory(
                        "Backpack",
                        st.session_state.inventory,
                        st.session_state.storage,
                        stored_items,
                        BACKPACK_CAPACITY,
                        st.session_state.storage_capacity,
                        "Store →",
                        "backpack",
                    )
                    render_storage_inventory(
                        "Storage",
                        st.session_state.storage,
                        st.session_state.inventory,
                        stored_items,
                        st.session_state.storage_capacity,
                        BACKPACK_CAPACITY,
                        "Take ←",
                        "storage",
                    )

                st.markdown("---")
                st.markdown(
                    f"#### {icon_text('🛡️', 'Mouse defenses')}",
                    unsafe_allow_html=True,
                )
                insulation_level = st.session_state.mouse_insulation_level
                insulation_cost = {
                    "Dirt": 5 * (insulation_level + 1),
                    "Roots": 4 * (insulation_level + 1),
                }
                insulation_columns = st.columns([2, 1])
                with insulation_columns[0]:
                    st.write(f"**Insulation · Level {insulation_level}/3**")
                    st.caption(
                        "Protects stored supplies. At level 3, mice can no longer steal from storage."
                    )
                    st.caption("Next level: " + " · ".join(
                        f"{amount} {item} (have {st.session_state.inventory.get(item, 0)})"
                        for item, amount in insulation_cost.items()
                    ))
                with insulation_columns[1]:
                    insulation_ready = all(
                        st.session_state.inventory.get(item, 0) >= amount
                        for item, amount in insulation_cost.items()
                    )
                    if st.button(
                        "Upgrade insulation",
                        key="upgrade_insulation",
                        disabled=insulation_level >= 3 or not insulation_ready,
                    ):
                        purchase_storage_upgrade("insulation")
                        st.rerun()

                repellent_level = st.session_state.mouse_repellent_level
                repellent_cost = {
                    "Dead Flower": repellent_level + 1,
                    "Roots": 3 * (repellent_level + 1),
                }
                repellent_columns = st.columns([2, 1])
                with repellent_columns[0]:
                    st.write(f"**Mouse repellent · Level {repellent_level}/3**")
                    st.caption(
                        "Reduces raid chances; level 3 keeps mice away completely."
                    )
                    st.caption("Next level: " + " · ".join(
                        f"{amount} {item} (have {st.session_state.inventory.get(item, 0)})"
                        for item, amount in repellent_cost.items()
                    ))
                with repellent_columns[1]:
                    repellent_ready = all(
                        st.session_state.inventory.get(item, 0) >= amount
                        for item, amount in repellent_cost.items()
                    )
                    if st.button(
                        "Make repellent",
                        key="upgrade_mouse_repellent",
                        disabled=repellent_level >= 3 or not repellent_ready,
                    ):
                        purchase_storage_upgrade("repellent")
                        st.rerun()

    if st.session_state.message and time.time() < st.session_state.message_expiry:
        time.sleep(0.5)
        st.rerun()
    elif st.session_state.message and time.time() >= st.session_state.message_expiry:
        st.session_state.message = ""
