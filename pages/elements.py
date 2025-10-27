import st_yled
import streamlit as st

import uiconfig
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

elements_display = dict()

# TODO: Add ini defaults
elements_display['hash_value'] = {
    'name': 'button',
    'types' : {
        'primary': {
            'css' : {
                'background_color': None,
                'color': None,
                'font_size': None,
                'border_style': None,
                'border_color': None,
                'border_width': None,
            },
            'example': "st_yled.button(\"Style Me\", type=\"primary\", **kwargs)"
        },
        'secondary': {
            'css' : {
                'background_color': None,
                'color': None,
                'font_size': None,
                'border_style': None,
                'border_color': None,
                'border_width': None,
            },
            'example': "st_yled.button(\"Style Me\", type=\"secondary\", **kwargs)"
        },
        'tertiary': {
            'css' : {
                'background_color': None,
                'color': None,
                'font_size': None,
                'border_style': None,
                'border_color': None,
                'border_width': None,
            },
            'example': "st_yled.button(\"Style Me\", type=\"tertiary\", **kwargs)"
        }
    },
}




with st_yled.popover('Style element',
                    icon=":material/add_circle:",
                    background_color="#ff4b4b",
                    color="#ffffff",
                    key="elements-add-element-popover"):
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

        # Top Button Controls for Adding Element Styles

        but_cont = st.container(horizontal=True)

        but_cont.button(
            "Add to selection",
            key="elements-add-element-selection",
            type="primary",
        )

        st_yled.subheader('st.' + element_select)

        example_cont = st.container(horizontal_alignment="left")
        
        with example_cont:

            element_config = st_yled.styler.get_element_style(element_select)

            if 'example' in element_config:
                
                kwargs = {}
                eval(element_config['example'])


for element_key in elements_display.keys():
    
    element_card_props = elements_display[element_key]

    element_types = list(element_card_props['types'].keys())
    
    if len(element_types) == 1:
        type_selector = False
        type_select = element_types[0]
    else:
        type_selector = True
        if 'secondary' in element_types:
            type_select = 'secondary'
        else:
            type_select = element_types[0]

    # Get available css properties for this element type
    css_props = list(element_card_props['types'][type_select]['css'].keys())
    css_tabs = {uiconfig.css_properties_tabs[prop] for prop in css_props}

    tabs_render = []
    if 'Color' in css_tabs:
        tabs_render.append('Color')
    if 'Font' in css_tabs:
        tabs_render.append('Font')
    if 'Border' in css_tabs:
        tabs_render.append('Border')

    with st_yled.container(background_color='#F6F6F6'):

        col1, col2 = st.columns([1,2])

        with col1:
            st.subheader('st.' + element_card_props['name'])

            # Check if multiple types
            if type_selector:
                type_select = st_yled.selectbox(
                    "Select Type",
                    options=element_types,
                    index=element_types.index(type_select),
                    key=f"element-{element_key}-type-select",
                    format_func=lambda x: uiconfig.element_type_format.get(x),
                    label_visibility="collapsed"
                )
            else:
                st.write("")

            # Create example container
            with st_yled.container(horizontal_alignment="center"):
                
                kwargs = {}
                eval(element_card_props['types'][type_select]['example'])

            st.button("Copy Code")


        with col2:

            tabs = st.tabs(tabs_render)
            
            for ix, tab in enumerate(tabs):

                with tab:

                    st.write(f"**{tabs_render[ix]} Properties**")

                    for prop in css_props:
                        if uiconfig.css_properties_tabs[prop] == tabs_render[ix]:
                            display_name = uiconfig.css_properties_display_name.get(prop, prop)
                            
                            

                            st.write(display_name)

                # with tab:

                #     st.write(f"**{tab} Properties**")
                    
                #     # for prop in css_props:
                #     #     if uiconfig.css_properties_tabs[prop] == tab:
                #     #         display_name = uiconfig.css_properties_display_name.get(prop, prop)
                #     #         current_value = element_card_props['types'][type_select]['css'][prop]
                #     #         st_yled.text_input(
                #     #             display_name,
                #     #             value=current_value if current_value is not None else "",
                #     #             key=f"element-{element_key}-{type_select}-{prop}-input",
                #     #             label_visibility="visible"
                #     #         )
