import st_yled
import streamlit as st

import utils

# region data

if 'element-select' not in st.session_state:
    st.session_state['element-select'] = None

# Load all compoentns
# Load categories and related components

all_elements = st_yled.styler.get_stylable_elements(include_variants=False)
element_categories = st_yled.styler.get_stylable_elements_by_category()
category_options = list(element_categories.keys())

category_display_slug_map = utils.CATEGORY_SLUGS
category_slug_display_map = utils.revert_category_slugs()

# Get all display names for categories
category_display_options = [category_slug_display_map[cat] for cat in category_options]

# region UI

st.markdown("**> Elements** Customize Streamlit components app elements")

nav_cont = st.container(key="elements-nav-cont")

with st_yled.popover('Style element',
                    icon=":material/add_circle:",
                    background_color="#ff4b4b",
                    color="#ffffff"):
    cont = st.container(width=800)

    col1, col2 = cont.columns([1,1])

    with col1:
        # search_select = st_yled.selectbox(
        #     "Select element to style",
        #     options=all_elements,
        #     index=None,
        #     key="elements-search-select"
        # )

        col1_cat, col2_cat = col1.columns([1,2])

        with col1_cat:
            # Returns display names for categories
            category_select_display = st_yled.radio(
                "Select Category",
                options=category_display_options,
                key="elements-category-select",
                label_visibility="collapsed"
            )

        category_select = category_display_slug_map[category_select_display]
        cat_elements = element_categories[category_select]

        with col2_cat:
            element_select = st_yled.radio(
                "Select Element",
                options=cat_elements,
                key="elements-state-select",
                label_visibility="collapsed"
            )

    with col2:

        st_yled.subheader('st.' +element_select)

        element_config = st_yled.styler.get_element_style(element_select)

        if 'example' in element_config:
            
            kwargs = {}
            eval(element_config['example'])

