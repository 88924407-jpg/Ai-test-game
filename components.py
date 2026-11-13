# components.py
import base64
import html
import re
from functools import lru_cache

import streamlit as st
from data import ITEM_ENCYCLOPEDIA


_SPRITES = {
    "axe": ("...##...", "...##...", "..###...", ".####...", "#####...", "...##...", "...##...", "...##..."),
    "berries": ("........", "..##.##.", ".######.", ".######.", "..####..", "...##...", "..####..", "........"),
    "book": ("..####..", ".##..##.", ".##..##.", ".######.", ".##..##.", ".##..##.", ".######.", "........"),
    "bowl": ("........", ".######.", "##....##", ".######.", "..####..", "...##...", "........", "........"),
    "bow": ("..##....", ".#..#...", "#....#..", "#....#..", "#....#..", ".#..#...", "..##....", "...##..."),
    "brick": ("........", ".######.", ".##.##.#", "########", "##.##.##", "########", ".######.", "........"),
    "bug": ("...##...", ".######.", "########", "..####..", ".##..##.", "##....##", "........", "........"),
    "carrot": ("...##...", "..####..", "...##...", ".######.", "..####..", "...###..", "...##...", "...#...."),
    "club": ("...##...", "..####..", ".######.", "..####..", "...##...", "...##...", "..####..", ".######."),
    "coal": ("...##...", ".######.", "########", "########", ".######.", "..####..", "...##...", "........"),
    "cord": ("##......", ".##.....", "..##....", "...##...", "....##..", ".....##.", "......##", "........"),
    "crate": (".######.", "##....##", "##.##.##", "##.##.##", "##....##", "########", ".######.", "........"),
    "droplet": ("...##...", "..####..", ".######.", "########", "########", ".######.", "..####..", "...##..."),
    "feather": (".....##.", "...####.", "..#####.", ".######.", "..#####.", "...###..", "....##..", "....##.."),
    "fish": ("........", "...##...", ".######.", "########", ".######.", "...##...", "........", "........"),
    "flower": ("...##...", "..####..", ".##..##.", "..####..", "...##...", "########", "...##...", "..####.."),
    "gear": ("..####..", ".######.", "##.##.##", "########", "########", "##.##.##", ".######.", "..####.."),
    "grain": ("...##...", "..###...", "...##...", ".##.##..", "...##...", "..##.##.", "...##...", "....##.."),
    "hammer": ("..####..", "########", "..####..", "...##...", "...##...", "...##...", "...##...", "...##..."),
    "hook": ("..####..", ".##..##.", ".##......", ".##......", ".##......", ".##......", "..##.....", "...##...."),
    "jar": ("..####..", "..####..", ".######.", ".######.", ".######.", ".######.", "..####..", "........"),
    "leaf": ("....##..", "...####.", "..######", ".######.", "########", ".######.", "...##...", "..##...."),
    "meat": ("........", ".######.", "########", "########", ".######.", "..####..", "..##.##..", "........"),
    "metal": ("........", "..####..", ".######.", "########", "########", ".######.", "..####..", "........"),
    "mushroom": ("..####..", ".######.", "########", "...##...", "...##...", ".######.", ".######.", "........"),
    "net": ("#..#..#.", ".#..#..#", "#..#..#.", ".#..#..#", "#..#..#.", ".#..#..#", "#..#..#.", "........"),
    "pick": ("...##...", "..####..", ".##.##..", "##..##..", "....##..", "....##..", "....##..", "...###.."),
    "pie": ("........", "..####..", ".######.", "########", "########", "########", ".######.", "........"),
    "plant": ("...##...", "..####..", "...##...", "...##...", ".######.", "..####..", ".######.", "########"),
    "pouch": ("..####..", ".######.", "########", "########", "##.##.##", ".######.", "..####..", "........"),
    "rock": ("........", "...##...", "..####..", ".######.", "########", "########", ".######.", "........"),
    "scissors": ("##....##", ".##..##.", "..####..", "...##...", "...##...", "..####..", ".##..##.", "##....##"),
    "spear": ("...##...", "...##...", "...##...", "...##...", "...##...", "...##...", "...##...", "..####.."),
    "spark": ("...##...", "...##...", "########", "..####..", "..####..", "########", "...##...", "...##..."),
    "sword": ("...##...", "..####..", "...##...", "...##...", "...##...", "...##...", ".######.", "..####.."),
    "tent": ("...##...", "...##...", "..####..", "..####..", ".######.", ".######.", "########", "##....##"),
    "tooth": ("..####..", ".######.", ".######.", "..####..", "..####..", "...##...", "...##...", "........"),
    "tracks": ("##..##..", "##..##..", "........", "..##..##", "..##..##", "........", "##..##..", "##..##.."),
    "trap": ("########", "#......#", "#.####.#", "#.#..#.#", "#.####.#", "#......#", "########", "........"),
    "tree": ("...##...", "..####..", ".######.", "########", "..####..", "..####..", ".######.", "########"),
    "trident": ("#..##..#", ".#.##.#.", "..####..", "...##...", "...##...", "...##...", "...##...", "..####.."),
    "water": ("........", "...##...", "..####..", "...##...", "..####..", ".######.", "########", "........"),
    "wind": ("########", "........", ".######.", "........", "######..", "........", "..####..", "........"),
    "wood": ("########", "##....##", "##....##", "##....##", "##....##", "##....##", "########", "........"),
    "worm": ("........", "..####..", ".######.", "##....##", "..####..", ".######.", "........", "........"),
    "flame": ("...##...", "..####..", "..####..", ".######.", ".##..##.", ".######.", "..####..", "...##..."),
}

_PALETTES = {
    "axe": ("#D1A65C", "#80603B", "#F2D58C"),
    "berries": ("#8A4F86", "#553659", "#D99AC8"),
    "book": ("#78936A", "#405A45", "#C5D49C"),
    "bowl": ("#C98E55", "#805535", "#E9C07A"),
    "bow": ("#A66B42", "#64432E", "#D8A66A"),
    "brick": ("#B76F4C", "#774631", "#DEA17A"),
    "bug": ("#86A75C", "#4A683E", "#C5D982"),
    "carrot": ("#D98542", "#8A5133", "#9CB967"),
    "club": ("#A8794E", "#644A36", "#D5B37B"),
    "coal": ("#59666A", "#303A3C", "#A3B0AA"),
    "cord": ("#B68A55", "#745536", "#E0C18A"),
    "crate": ("#B28A53", "#725635", "#D9B973"),
    "droplet": ("#5797A2", "#37616C", "#A5D8D5"),
    "feather": ("#86A86B", "#4D6B4E", "#D4DCA3"),
    "fish": ("#6C9FA5", "#3B6870", "#B4D9C9"),
    "flower": ("#C86E78", "#78444C", "#F0B77D"),
    "gear": ("#9B9A75", "#5C6655", "#D7C983"),
    "grain": ("#C6A64E", "#7A6538", "#EBD58A"),
    "hammer": ("#8C8E83", "#555C56", "#D1BE8A"),
    "hook": ("#A9A99A", "#626C68", "#DBD5B4"),
    "jar": ("#83A99C", "#4F7068", "#C4D7B3"),
    "leaf": ("#6F9A5E", "#426447", "#B5CB78"),
    "meat": ("#B76C59", "#74483E", "#E3A17D"),
    "metal": ("#9AABB0", "#5A6D73", "#D8DAD0"),
    "mushroom": ("#C98369", "#765347", "#E8C994"),
    "net": ("#819985", "#4B6452", "#C7D0A1"),
    "pick": ("#9A875D", "#5C503D", "#D8B66E"),
    "pie": ("#BD8154", "#76513D", "#E9C783"),
    "plant": ("#72995D", "#456443", "#C1D483"),
    "pouch": ("#A87958", "#694C3B", "#D7B77F"),
    "rock": ("#8B9690", "#59635E", "#C7C6A8"),
    "scissors": ("#94A5A4", "#5B6A69", "#D1D8C7"),
    "spear": ("#A8895D", "#604C38", "#D3BE83"),
    "spark": ("#D7A746", "#896333", "#F5DB86"),
    "sword": ("#AAB8B3", "#5B6D68", "#DFD5A9"),
    "tent": ("#B9784D", "#6F4A38", "#D6B477"),
    "tooth": ("#C5BDA0", "#786E5D", "#F2EBD4"),
    "tracks": ("#9B7958", "#624B38", "#D0A86C"),
    "trap": ("#A77A4E", "#624B37", "#D6B777"),
    "tree": ("#688D5C", "#405E43", "#B2C77C"),
    "trident": ("#A6B6AE", "#5D6E66", "#DDCF9F"),
    "water": ("#5797A2", "#37616C", "#A5D8D5"),
    "wind": ("#87A8A2", "#526E68", "#C4D9C9"),
    "wood": ("#A9784B", "#65472F", "#D3AD70"),
    "worm": ("#B46E68", "#724B48", "#E2A28A"),
    "flame": ("#D98542", "#8A5133", "#F2C45E"),
}

_ICON_FAMILY = {
    "🟤": "rock", "🟫": "rock", "⬛": "coal", "🪨": "rock", "🪵": "wood",
    "🧱": "brick", "🔩": "metal", "✨": "spark", "♨️": "flame", "💧": "water",
    "🐛": "worm", "🪱": "worm", "🐾": "tracks", "👣": "tracks", "🐟": "fish",
    "🐗": "meat", "🦌": "trident", "🦷": "tooth", "🌿": "leaf", "🍃": "leaf",
    "🍂": "leaf", "🌱": "plant", "🪴": "plant", "🌾": "grain", "🥕": "carrot",
    "🥀": "flower", "🌹": "flower", "🌼": "flower", "🍄": "mushroom", "🫐": "berries",
    "🥜": "berries", "🍖": "meat", "🥩": "meat", "🍯": "berries", "🥧": "pie",
    "🍲": "bowl", "🥣": "bowl", "🍴": "trident", "⚔️": "sword", "🗡️": "sword",
    "🔪": "sword", "🔱": "trident", "🏹": "bow", "🏏": "club", "🔨": "hammer",
    "🪓": "axe", "🪚": "spear", "🪒": "pick", "🪝": "hook", "🪢": "cord",
    "🧵": "cord", "🧶": "cord", "🕸️": "net", "🎣": "spear", "🪶": "feather",
    "👝": "pouch", "🧺": "crate", "🏺": "jar", "🪹": "crate", "🪤": "trap",
    "🚜": "wood", "🛶": "wood", "⚓": "trident", "⚙️": "gear", "⛰️": "rock",
    "⛺": "tent", "🌬️": "wind", "🌳": "tree", "📋": "book", "📖": "book",
    "🔔": "spark", "🎯": "spark", "🎒": "crate", "📦": "crate", "🦴": "tooth",
    "🐭": "worm", "🖱️": "gear", "👏": "spark", "🛡️": "metal", "🎉": "spark",
    "📌": "pick", "⚙": "gear", "🎨": "flower", "⛏️": "pick", "🧪": "jar",
    "🚀": "wood", "🔊": "wind", "🏠": "tent", "📜": "book", "♾️": "cord",
    "⚡": "spark", "✅": "leaf", "🟢": "leaf", "🧭": "gear", "🔒": "metal",
    "🏕️": "tent", "🗃️": "crate", "🛠️": "hammer", "⬆️": "spear", "🖱": "gear",
    "🛡": "metal", "✂️": "scissors", "🔥": "flame",
}

PIXEL_ICON_CHOICES = {
    "Stone": "🪨", "Soil": "🟤", "Plant": "🌿", "Flower": "🌼",
    "Mushroom": "🍄", "Carrot": "🥕", "Berries": "🫐", "Fish": "🐟",
    "Meat": "🍖", "Tool": "🪓", "Weapon": "⚔️", "Bow": "🏹",
    "Fishing gear": "🎣", "Basket": "🧺", "Bottle": "🏺", "Fire": "🔥",
    "Spark": "✨", "Rope": "🪢", "Brick": "🧱",
}

_EXTRA_SPRITES = {
    "dirt": (("..####..", ".########", "########", "########", ".######.", "..####..", "...##...", "........"), ("#9B7652", "#634A37", "#C9A97C")),
    "heat": (("...##...", "..####..", ".##..##.", ".##..##.", "..####..", "...##...", "..####..", ".######."), ("#D68E42", "#8F4D35", "#F1C66D")),
    "boar": (("##....##", "########", "##.##.##", "########", ".######.", "..####..", "...##...", "........"), ("#A66F52", "#624939", "#D5A177")),
    "antler": (("#..##..#", ".#.##.#.", "..####..", "...##...", "..####..", ".##..##.", "##....##", "........"), ("#B99A65", "#705C40", "#E0C98E")),
    "honey": (("........", ".######.", "########", "##.##.##", "########", ".######.", "..####..", "........"), ("#D19A43", "#835D2D", "#F0CC71")),
    "fork": (("#.#..#.#", "#.#..#.#", "..####..", "...##...", "...##...", "...##...", "...##...", "...##..."), ("#AEB5A9", "#65736A", "#E0D3A4")),
    "saw": (("........", "########", "#.#.#.#.", "...##...", "...##...", "...##...", "...##...", "..####.."), ("#AEB5A9", "#65736A", "#E0D3A4")),
    "rod": (("#.......", ".#......", "..#.....", "...#....", "....#...", ".....#..", "......#.", ".......#"), ("#A77B4E", "#624730", "#D6AF74")),
    "nest": (("##....##", ".##..##.", "..####..", ".######.", "##....##", ".######.", "..####..", "........"), ("#A77B4E", "#624730", "#D6AF74")),
    "cart": (("########", "#......#", "########", "...##...", "...##...", "........", ".##..##.", ".##..##."), ("#A77B4E", "#624730", "#D6AF74")),
    "boat": (("........", "##....##", ".######.", "..####..", "...##...", "..####..", ".######.", "########"), ("#6E9BA2", "#3E6670", "#B8D7C8")),
    "anchor": (("...##...", "...##...", "########", "...##...", ".##.##..", "##...##.", "........", "........"), ("#AEB5A9", "#65736A", "#E0D3A4")),
    "arrow": ((".......#", "......##", ".....###", "....####", "...##...", "..##....", ".##.....", "##......"), ("#85A469", "#4A674A", "#C6D28C")),
}

for _family, (_rows, _palette) in _EXTRA_SPRITES.items():
    _SPRITES[_family] = _rows
    _PALETTES[_family] = _palette


@lru_cache(maxsize=256)
def pixel_icon_data_uri(icon, label="", style="Advanced Simple"):
    family = _ICON_FAMILY.get(icon, "crate")
    rows = _SPRITES.get(family, _SPRITES["crate"])
    palette = _PALETTES.get(family, _PALETTES["crate"])
    if style == "Pixel Art":
        pixels = []
        for y, row in enumerate(rows):
            for x, pixel in enumerate(row):
                if pixel == ".":
                    continue
                color = palette[2] if (x + y) % 4 == 0 else palette[1] if y > 4 else palette[0]
                pixels.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{color}"/>')
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 8" '
            f'role="img" aria-label="{html.escape(label, quote=True)}" shape-rendering="crispEdges">'
            + "".join(pixels) + "</svg>"
        )
        return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode("ascii")

    illustrated = style == "Soft Illustrated"
    card_start, card_end = (
        ("#FFF8EE", "#F2E6D5") if illustrated else ("#FFFDF5", "#E8ECDD")
    )
    corner_radius = "1.8" if illustrated else "1.25"
    pixels = []
    for y, row in enumerate(rows):
        for x, pixel in enumerate(row):
            if pixel != ".":
                color = palette[2] if (x + y) % 4 == 0 else palette[1] if y > 4 else palette[0]
                pixels.append(
                    f'<rect x="{x * 5 + 8}" y="{y * 5 + 8}" width="4.65" height="4.65" '
                    f'rx="{corner_radius}" fill="{color}" stroke="#493D30" stroke-opacity=".16" stroke-width=".25"/>'
                )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56" '
        f'role="img" aria-label="{html.escape(label, quote=True)}">'
        '<defs><linearGradient id="card" x1="0" y1="0" x2="1" y2="1">'
        f'<stop stop-color="{card_start}"/><stop offset="1" stop-color="{card_end}"/>'
        '</linearGradient><linearGradient id="shine" x1="0" y1="0" x2="0" y2="1">'
        '<stop stop-color="#FFF" stop-opacity=".8"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/>'
        '</linearGradient><filter id="shadow" x="-30%" y="-30%" width="160%" height="170%">'
        '<feDropShadow dx="0" dy="2" stdDeviation="1.5" flood-color="#263A35" flood-opacity=".16"/>'
        '</filter></defs><rect x="3" y="3" width="50" height="50" rx="14" fill="url(#card)" '
        'stroke="#D8DDCF" stroke-width="1.2" filter="url(#shadow)"/>'
        '<path d="M17 4h22a14 14 0 0 1 14 14v4H3v-4A14 14 0 0 1 17 4" fill="url(#shine)"/>'
        + "".join(pixels) + "</svg>"
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode("ascii")


def pixel_icon_html(icon, label="", size=32, style="Advanced Simple"):
    alt = html.escape(label, quote=True)
    return (
        f'<img class="pixel-icon" src="{pixel_icon_data_uri(icon, label, style)}" '
        f'alt="{alt}" width="{size}" height="{size}" '
        'style="image-rendering:auto;vertical-align:middle;">'
    )


def paper_drawing_html(icon, label, size=94, style="Advanced Simple"):
    family = _ICON_FAMILY.get(icon, "plant")
    rows = _SPRITES.get(family, _SPRITES["plant"])
    palette = _PALETTES.get(family, _PALETTES["plant"])
    rounding = ".12" if style == "Pixel Art" else ".55" if style == "Soft Illustrated" else ".35"
    drawing = []
    for y, row in enumerate(rows):
        for x, pixel in enumerate(row):
            if pixel != ".":
                color = palette[2] if (x + y) % 4 == 0 else palette[1] if y > 4 else palette[0]
                drawing.append(
                    f'<rect x="{x * 2 + 5}" y="{y * 2 + 2}" width="1.85" height="1.85" '
                    f'rx="{rounding}" fill="{color}"/>'
                )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 26 28">'
        '<path d="M4 1.5h13l5 5V25a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 4 25z" '
        'fill="#FFF9E9" stroke="#9D815B" stroke-width=".8"/>'
        '<path d="M17 1.8v4a1 1 0 0 0 1 1h4" fill="#E9DAB9" stroke="#9D815B" stroke-width=".7"/>'
        + "".join(drawing)
        + '<path d="M7 21h12M7 23h9" stroke="#C5AE86" stroke-width=".55" stroke-linecap="round"/>'
        '</svg>'
    )
    encoded = base64.b64encode(svg.encode()).decode("ascii")
    alt = html.escape(label, quote=True)
    return (
        f'<img class="illustrated-paper" src="data:image/svg+xml;base64,{encoded}" '
        f'alt="{alt}" title="{alt}" width="{size}" height="{size}">'
    )


def safe_widget_key(key):
    return re.sub(r"[^A-Za-z0-9_-]", lambda match: f"_u{ord(match.group()):x}_", key)


def icon_button_style(icon, label, style="Advanced Simple"):
    label = safe_widget_key(label)
    return (
        f'<style>.st-key-{label} button::before{{content:"";display:inline-block;'
        'width:22px;height:22px;flex:0 0 22px;margin-right:8px;'
        f'background:url("{pixel_icon_data_uri(icon, label, style)}") center/contain no-repeat;'
        'image-rendering:auto;vertical-align:middle;}}</style>'
    )


def icon_text(icon, label, size=26, style="Advanced Simple"):
    return (
        '<span class="pixel-label">'
        f'{pixel_icon_html(icon, label, size, style)} {html.escape(label)}'
        '</span>'
    )


def replace_icons(text):
    text = html.escape(text)
    for icon in sorted(_ICON_FAMILY, key=len, reverse=True):
        escaped_icon = html.escape(icon)
        if escaped_icon in text:
            text = text.replace(escaped_icon, pixel_icon_html(icon, icon, 20))
    return text

@st.dialog("Backpack Inventory", width="large")
def inventory_modal():
    art_style = st.session_state.get("ui_settings", {}).get(
        "art_style", "Advanced Simple"
    )
    st.markdown(
        f"### {pixel_icon_html('🎒', 'Backpack Inventory', 32, art_style)} Backpack Inventory",
        unsafe_allow_html=True,
    )
    backpack_load = sum(max(0, count) for count in st.session_state.inventory.values())
    st.caption(f"Backpack capacity: {backpack_load}/{st.session_state.get('backpack_capacity', 200)} items")
    categories = [
        ("all", "All"), ("material", "Materials"), ("food", "Food"),
        ("crafted", "Crafted"), ("tool", "Tools"), ("weapon", "Weapons"),
        ("fishing", "Fishing"), ("farming", "Farming"), ("hunting", "Hunting"),
        ("research", "Research"),
    ]
    for start in range(0, len(categories), 5):
        category_row = categories[start:start + 5]
        tab_cols = st.columns(len(category_row))
        for column, (cat_key, cat_label) in zip(tab_cols, category_row):
            with column:
                if st.button(cat_label, key=f"tab_btn_{cat_key}"):
                    st.session_state.inv_tab = cat_key
                    st.rerun()

    st.markdown("---")

    sort_col1, sort_col2 = st.columns(2)
    with sort_col1:
        st.session_state.inv_sort_by = st.selectbox("Sort by", ["Rarity", "Name", "Amount"], key="sort_by_select")
    with sort_col2:
        st.session_state.inv_sort_order = st.selectbox("Order", ["Standard (Ascending)", "Reverse (Descending)"], key="sort_order_select")

    st.markdown("---")

    items_to_display = []
    rarity_weight = {"Common": 1, "Uncommon": 2, "Rare": 3, "Crafted": 4}

    for item_name, count in st.session_state.inventory.items():
        if count <= 0:
            continue
            
        meta = ITEM_ENCYCLOPEDIA.get(item_name, {"rarity": "Common", "category": "material", "icon": "📦", "description": "Unknown item.", "use": "Unknown use.", "color": "#F0F0F0"})
        if st.session_state.inv_tab != "all" and meta["category"] != st.session_state.inv_tab:
            continue
            
        # Check if user set a custom color override in session state
        custom_colors = st.session_state.get("item_custom_colors", {})
        item_bg = custom_colors.get(item_name, meta.get("color", "#F0F0F0"))

        items_to_display.append({
            "name": item_name,
            "count": count,
            "rarity": meta["rarity"],
            "rarity_weight": rarity_weight.get(meta["rarity"], 1),
            "icon": meta["icon"],
            "description": meta["description"],
            "use": meta["use"],
            "color": item_bg
        })

    reverse_bool = "Reverse" in st.session_state.inv_sort_order
    if st.session_state.inv_sort_by == "Name":
        items_to_display.sort(key=lambda x: x["name"], reverse=reverse_bool)
    elif st.session_state.inv_sort_by == "Amount":
        items_to_display.sort(key=lambda x: x["count"], reverse=reverse_bool)
    else:
        items_to_display.sort(key=lambda x: x["rarity_weight"], reverse=reverse_bool)

    if not items_to_display:
        st.info("No discovered items in this category yet. Go dig in the cave!")
    else:
        cols_per_row = 4
        rows = [items_to_display[i:i + cols_per_row] for i in range(0, len(items_to_display), cols_per_row)]
        
        for row in rows:
            cols = st.columns(cols_per_row)
            for idx, item in enumerate(row):
                with cols[idx]:
                    # Render custom colored card container using HTML wrapper
                    st.markdown(f"""
                        <div class="inventory-card" style="background-color: {item['color']};">
                            <b>{pixel_icon_html(item['icon'], item['name'], 28, art_style)} {item['name']}</b><br>
                            <span style="font-size: 0.9rem;">Quantity: {item['count']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    button_label = f"Inspect {item['name']}"
                    button_key = safe_widget_key(f"inv_click_{item['name']}")
                    st.markdown(
                        icon_button_style(item["icon"], button_key, art_style),
                        unsafe_allow_html=True,
                    )
                    if st.button(button_label, key=button_key, help=f"{item['description']}\n\nUse: {item['use']}"):
                        st.session_state.selected_item = item['name']
                        st.session_state.show_inventory_modal = False
                        st.rerun()
