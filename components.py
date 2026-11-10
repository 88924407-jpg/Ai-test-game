# components.py
import streamlit as st
from data import ITEM_ENCYCLOPEDIA

@st.dialog("🎒 Backpack Inventory", width="large")
def inventory_modal():
    tab_cols = st.columns(5)
    categories = [("all", "All"), ("material", "Materials"), ("food", "Food"), ("crafted", "Crafted"), ("tool", "Tools")]
    for i, (cat_key, cat_label) in enumerate(categories):
        with tab_cols[i]:
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
                        <div style="background-color: {item['color']}; padding: 10px; border-radius: 8px; border: 1px solid rgba(0,0,0,0.1); margin-bottom: 5px; text-align: center;">
                            <b>{item['icon']} {item['name']}</b><br>
                            <span style="font-size: 0.9rem;">📦 x{item['count']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    button_label = f"Inspect {item['name']}"
                    if st.button(button_label, key=f"inv_click_{item['name']}", help=f"{item['description']}\n\nUse: {item['use']}"):
                        st.session_state.selected_item = item['name']
                        st.session_state.show_inventory_modal = False
                        st.rerun()