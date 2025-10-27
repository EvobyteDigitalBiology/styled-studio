
import uuid
import st_yled
import streamlit as st

import uiconfig
import utils

import re

def elements_color_picker(elements_key: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 140):

    if elements_key in st.session_state:
        color_state_value = st.session_state[elements_key]
        code_color = None
    else:
        color_state_value = "default"
        code_color = "grey"

    utils.base_color_picker(
        key=elements_key,
        label=label,
        label_font_size=label_font_size,
        label_field_width=label_field_width,
        color_state_value=color_state_value,
        code_color=code_color
    )

def elements_selectbox(key: str,
                        label: str,
                        options: list[str],
                        label_font_size: str = '16px',
                        label_field_width: int = 140):

    with st.container(horizontal=True, vertical_alignment="center"):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        selected_option = st_yled.selectbox(
            "Select an option",
            options=options,
            index=None,
            key=key + "-selectbox",
            label_visibility="collapsed",
            on_change=utils.update_st_from_input,
            args=(key, key + "-selectbox"),
            width = 180
        )

        st_yled.caption("Select Option", width=100)


def elements_size_input(key,
                        label: str,
                        allowed_units: list[str],
                        unit_step_sizes: list[float],
                        label_font_size: str = '16px',
                        label_field_width: int = 140):

    if key in st.session_state:
        size_state_value = st.session_state[key]
        
        current_number = re.findall(r'\d+\.?\d*', size_state_value)[0]
        current_number = float(current_number)
        current_unit = re.findall(r'[a-zA-Z]+', size_state_value)[0]
    else:
        current_number = None
        current_unit = allowed_units[0]

    input_seed_key = key + "-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    step_size = unit_step_sizes[allowed_units.index(current_unit)]

    utils.base_size_input(
        key=key,
        seed_value=st.session_state[input_seed_key],
        label=label,
        value=current_number,
        step_size=step_size,
        unit=current_unit,
        allowed_units=allowed_units,
        label_font_size=label_font_size,
        label_field_width=label_field_width,
        return_value_type='str'
    )


def get_input_widget_for_property(prop: str, key: str, display_name: str):

    widget_type = uiconfig.css_properties_input_widget[prop]
    
    if widget_type == 'color_picker':
        elements_color_picker(key, display_name, label_font_size='16px')
    elif widget_type == 'size_input':
        allowed_units = ['px', 'em', 'rem']
        unit_step_sizes = [1.0, 0.1, 0.1]
        elements_size_input(
            key,
            display_name,
            allowed_units,
            unit_step_sizes,
            label_font_size='16px'
        )
    elif widget_type == 'selectbox':
        if prop == 'border_style':
            options = ['none', 'solid', 'dashed', 'dotted', 'double', 'groove', 'ridge', 'inset', 'outset']
            elements_selectbox(key, display_name, options, label_font_size='16px')
    else:
        pass


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
    
    element_name = element_card_props['name']

    # Check if multiple types
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
            st.subheader('st_yled.' + element_name)

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

            if type_selector:
                element_key_base = 'element-' + element_name + "-" + type_select
            else:
                element_key_base = element_name
            
            # Create example container
            with st_yled.container(horizontal_alignment="center"):
                
                kwargs = {}
                # Extract all css properties for this element type
                for key in st.session_state.keys():
                    if key.startswith(element_key_base) and key.endswith("-value"):
                        css_prop = key.replace(element_key_base + '-', "").replace('-value', "")
                        css_value = st.session_state[key]
                        kwargs[css_prop] = css_value
                
                eval(element_card_props['types'][type_select]['example'])

            st.button("Copy Code")


        with col2:

            tabs = st.tabs(tabs_render)
            
            for ix, tab in enumerate(tabs):

                with tab:

                    for prop in css_props:
                        if uiconfig.css_properties_tabs[prop] == tabs_render[ix]:
                            display_name = uiconfig.css_properties_display_name.get(prop, prop)

                            element_key = element_key_base + f"-{prop}-value"

                            get_input_widget_for_property(prop, element_key, display_name)

                            # Get the right display function and def
